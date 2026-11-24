import hashlib
import logging

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

from alexandria.core.api import create_file
from alexandria.core.models import Document, File
from alexandria.core.utils import get_user_and_group_from_request

from . import models, pdf
from .backends import get_backend
from .permissions import SIGN, has_document_permission

log = logging.getLogger(__name__)

SIGNABLE_MIME_TYPES = ("application/pdf",)


def is_signable(file: File) -> bool:
    return (
        file.variant == File.Variant.ORIGINAL and file.mime_type in SIGNABLE_MIME_TYPES
    )


class OutdatedFileError(APIException):
    """The file to sign is no longer the latest version of its document."""

    status_code = 409
    default_detail = _(
        "The document was changed, only the latest version can be signed."
    )
    default_code = "outdated_file"


def _originals(document: Document) -> list[File]:
    """Return the original files of `document`, newest first.

    Not `document.get_latest_original()`: it queries the database (count +
    latest) and ignores prefetched files, which would add queries per
    document to list responses. Cached on the instance, so `can_sign` and
    `current_files` share it.
    """
    if not hasattr(document, "_esign_originals"):
        document._esign_originals = sorted(
            (f for f in document.files.all() if f.variant == File.Variant.ORIGINAL),
            key=lambda f: f.created_at,
            reverse=True,
        )
    return document._esign_originals


def _current(document: Document) -> list[tuple[File, list[models.Signature]]]:
    """Return the current versions with the signatures that created them."""
    if not hasattr(document, "_esign_current"):
        current = []
        for file in _originals(document):
            signatures = list(file.signatures.all())
            current.append((file, signatures))
            if not signatures:
                # Not created by signing or stamping
                break
        document._esign_current = current
    return document._esign_current


def current_files(document: Document) -> list[File]:
    """Return the versions whose signatures are still part of the latest file.

    Signing and stamping add incremental updates, so the latest version
    still contains the signatures of the versions below it, as long as every
    newer version was created by signing or stamping. Any other new version
    (replace, WebDAV, conversion) is a change unrelated to signatures and
    invalidates everything before it.

    Uses `files` and `files__signatures` if prefetched.
    """
    return [file for file, _signatures in _current(document)]


def current_signatures(document: Document) -> list[models.Signature]:
    """Return the signatures still contained in the latest file."""
    return [s for _file, signatures in _current(document) for s in signatures]


def is_latest(file: File) -> bool:
    """Return whether `file` is the latest original of its document.

    Queries the database, signing an older version would store its content
    as newest version and undo later changes.
    """
    latest = (
        File.objects.filter(document_id=file.document_id, variant=File.Variant.ORIGINAL)
        .order_by("-created_at")
        .values_list("pk", flat=True)
        .first()
    )
    return latest == file.pk


def end_expired_request(signature_request: models.SignatureRequest) -> None:
    """End an active request after its timeout, so it no longer blocks the file.

    Asks the backend for the final state (the user may have confirmed in the
    meantime). If that fails, the request is ended anyway.
    """
    if (
        not signature_request.is_active
        # Not started at the provider yet
        or signature_request.timeout is None
        or signature_request.timeout > timezone.now()
    ):
        return

    backend = get_backend()
    try:
        if backend:
            backend.cancel_signature(signature_request)
    except Exception:
        log.exception("Cleanup of signature request %s failed", signature_request.pk)

    if signature_request.is_active:
        signature_request.status = models.SignatureRequest.Status.TIMEOUT
        signature_request.prepared_content = None
    signature_request.save()


def can_sign(document: Document, request, cache: dict | None = None) -> bool:
    """Return whether the user of `request` can sign the latest file.

    `cache` keeps the group check across documents of the same request.
    """
    _user, group = get_user_and_group_from_request(request)
    if not group:
        return False

    originals = _originals(document)
    if not originals or not is_signable(originals[0]):
        return False

    cache = {} if cache is None else cache
    if group not in cache:
        backend = get_backend()
        cache[group] = backend is not None and backend.is_enabled_for(group)

    return cache[group] and has_document_permission(request, document, SIGN)


@transaction.atomic()
def stamp_file(
    file: File, user: str | None, group: str | None, data: dict | None = None
) -> models.Signature:
    """Stamp `file` and record it as finished signature request.

    `data` is passed to the backend, e.g. a visible stamp image.

    The request makes stamps appear next to signatures in the history of
    the file. It is created afterwards, so a running signature request on
    the same file does not block stamping.
    """
    backend = get_backend()
    if backend is None:
        raise ImproperlyConfigured("`ALEXANDRIA_ESIGN_BACKEND` is required to stamp")
    signature = backend.stamp(file, user=user, group=group, data=data or {})
    signature.signature_request = models.SignatureRequest.objects.create(
        file=file,
        # Decided by the backend, e.g. a timestamp or a qualified seal
        signature_type=signature.signature_type,
        status=models.SignatureRequest.Status.DONE,
        created_by_user=user,
        created_by_group=group,
        modified_by_user=user,
        modified_by_group=group,
    )
    signature.save()
    return signature


@transaction.atomic()
def store_signed_file(
    original: File,
    content: bytes,
    signature: bytes,
    signature_type: models.Signature.Type,
    user: str | None,
    group: str | None,
    signature_request: models.SignatureRequest | None = None,
) -> models.Signature:
    """Store the signed PDF as new version of the document.

    The original file stays untouched. Signer name and date are read from
    the embedded signature, so they may differ from the requesting user.
    A given `signature_request` is finished (caller saves it).
    """
    if not is_latest(original):
        # Would undo the changes of the newer version
        raise OutdatedFileError()
    signed_file = create_file(
        document=original.document,
        user=user,
        group=group,
        name=original.name,
        content=ContentFile(content, name=original.name),
        mime_type=original.mime_type,
        size=len(content),
    )

    embedded = pdf.last_signature(content)
    result = models.Signature.objects.create(
        file=signed_file,
        signature_request=signature_request,
        signature_type=signature_type,
        signer_name=embedded.signer_name or "",
        signed_at=embedded.signed_at or timezone.now(),
        signature_hash=hashlib.sha256(signature).hexdigest(),
        created_by_user=user,
        created_by_group=group,
        modified_by_user=user,
        modified_by_group=group,
    )

    if signature_request:
        signature_request.status = models.SignatureRequest.Status.DONE
        signature_request.prepared_content = None

    return result

import hashlib

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

from alexandria.core.api import create_file
from alexandria.core.models import Document, File
from alexandria.core.utils import get_user_and_group_from_request

from . import models, pdf
from .backends import get_backend
from .permissions import SIGN, has_document_permission

SIGNABLE_MIME_TYPES = ("application/pdf",)


def is_signable(file: File) -> bool:
    return (
        file.variant == File.Variant.ORIGINAL and file.mime_type in SIGNABLE_MIME_TYPES
    )


def _originals(document: Document) -> list[File]:
    """Return the original files of `document`, newest first.

    Not `document.get_latest_original()`: it queries the database (count +
    latest) and ignores prefetched files, which would add queries per
    document to list responses.
    """
    return sorted(
        (f for f in document.files.all() if f.variant == File.Variant.ORIGINAL),
        key=lambda f: f.created_at,
        reverse=True,
    )


def current_files(document: Document) -> list[File]:
    """Return the versions whose signatures are still part of the latest file.

    Signing and stamping add incremental updates, so the latest version
    still contains the signatures of the versions below it, as long as every
    newer version was created by signing or stamping. Any other new version
    (replace, WebDAV, conversion) is a change unrelated to signatures and
    invalidates everything before it.

    Uses `files` and `files__signatures` if prefetched.
    """
    current = []
    for file in _originals(document):
        current.append(file)
        if not file.signatures.all():
            # Not created by signing or stamping
            break
    return current


def current_signatures(document: Document) -> list[models.Signature]:
    """Return the signatures still contained in the latest file."""
    return [s for file in current_files(document) for s in file.signatures.all()]


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

    `data` is passed to the backend, e.g. the stamp image for DeepSign (see
    `DeepSignBackend.stamp`).

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

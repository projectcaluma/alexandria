import base64
import json
import logging
import time
import uuid
from datetime import timedelta
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.utils.module_loading import import_string

from alexandria.esign import pdf
from alexandria.esign.api import store_signed_file
from alexandria.esign.models import (
    DeepSignServiceAccount,
    Signature,
    SignatureRequest,
)

from .base import SignatureBackend, SignatureProviderError

log = logging.getLogger(__name__)

TOKEN_EXPIRY_MARGIN_SECONDS = 30

# Stamps are not confirmed by a person. If DeepSign does not return the
# signature right away, the status is polled this many times.
STAMP_STATUS_ATTEMPTS = 5
STAMP_STATUS_INTERVAL_SECONDS = 1


def build_connection_url(account: DeepSignServiceAccount) -> str:
    """Return the DeepSign URL to create a service account for `account.group`.

    DeepSign posts the credentials to `ALEXANDRIA_DEEPSIGN_CALLBACK_URL`,
    passing `state` back unchanged.
    """
    params = {
        "response_type": "service_account",
        "client_id": settings.ALEXANDRIA_DEEPSIGN_PARTNER_CLIENT_ID,
        "response_mode": "form_post",
        "redirect_uri": settings.ALEXANDRIA_DEEPSIGN_CALLBACK_URL,
        "state": json.dumps({"group": account.group, "token": account.state_token}),
    }
    return f"{settings.ALEXANDRIA_DEEPSIGN_CONNECTION_URL}?{urlencode(params)}"


class DeepSignClient:
    """Minimal client for the DeepSign hash signing API."""

    STATUS_SIGNED = "signed"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_REJECTED = "rejected"

    MODE_TIMESTAMP = "timestamp"

    def __init__(self, account: DeepSignServiceAccount):
        for setting in (
            "ALEXANDRIA_DEEPSIGN_TOKEN_URL",
            "ALEXANDRIA_DEEPSIGN_GATEWAY_URL",
            "ALEXANDRIA_DEEPSIGN_SIGN_URL",
        ):
            if not getattr(settings, setting):
                raise ImproperlyConfigured(f"`{setting}` is required for DeepSign")

        self.account = account
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self._get_access_token()}"

    def _request(self, method, url, **kwargs):
        try:
            response = self.session.request(
                method,
                url,
                timeout=settings.ALEXANDRIA_DEEPSIGN_HTTP_TIMEOUT_SECONDS,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as e:
            log.exception("DeepSign request to %s failed", url)
            raise SignatureProviderError() from e

    def _get_access_token(self) -> str:
        """Return a cached access token, or request a new one.

        DeepSign asks to reuse the token until it expires. The username is
        part of the key, so reconnecting the account invalidates the token.
        """
        cache_key = f"esign:deepsign:token:{self.account.pk}:{self.account.username}"
        if token := cache.get(cache_key):
            return token

        try:
            response = requests.post(
                settings.ALEXANDRIA_DEEPSIGN_TOKEN_URL,
                data={
                    "grant_type": "password",
                    "client_id": settings.ALEXANDRIA_DEEPSIGN_PARTNER_CLIENT_ID,
                    "client_secret": settings.ALEXANDRIA_DEEPSIGN_PARTNER_CLIENT_SECRET,
                    "username": self.account.username,
                    "password": self.account.password,
                },
                timeout=settings.ALEXANDRIA_DEEPSIGN_HTTP_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            data = response.json()
            token = data["access_token"]
            expires_in = int(data.get("expires_in", 0))
        except (requests.RequestException, ValueError, KeyError, TypeError) as e:
            log.exception("DeepSign authentication for %s failed", self.account)
            raise SignatureProviderError() from e

        # Margin, so a token does not expire between cache lookup and use
        if expires_in > TOKEN_EXPIRY_MARGIN_SECONDS:
            cache.set(cache_key, token, expires_in - TOKEN_EXPIRY_MARGIN_SECONDS)
        return token

    def register_person(self, person_ref: str) -> dict:
        """Return `personIdentityUid`, or `registrationDeepLink` if not registered."""
        return self._request(
            "POST",
            f"{settings.ALEXANDRIA_DEEPSIGN_GATEWAY_URL}/persons/register",
            json={"personRef": person_ref},
        )

    def sign_hash(
        self,
        hash_id: str,
        digest: bytes,
        document_name: str,
        signature_mode: str,
        identity_uid: str | None = None,
    ) -> dict:
        """Request a signature for `digest`.

        `identity_uid` identifies the signing person (DeepID) for advanced
        and qualified signatures, timestamps don't need it.
        """
        body = {
            "hashes": [
                {
                    "hashId": hash_id,
                    "digestValue": base64.b64encode(digest).decode("ascii"),
                    "digestAlgorithm": "SHA-512",
                }
            ],
            "signatureMode": signature_mode,
            "jurisdiction": settings.ALEXANDRIA_DEEPSIGN_JURISDICTION,
            "documentName": document_name,
        }
        if identity_uid:
            body["authorityService"] = "did"
            body["didIdentityId"] = identity_uid

        return self._request(
            "POST",
            f"{settings.ALEXANDRIA_DEEPSIGN_SIGN_URL}/service/hash/sign",
            json=body,
        )

    def get_status(self, hash_key: str) -> dict:
        return self._request(
            "GET",
            f"{settings.ALEXANDRIA_DEEPSIGN_SIGN_URL}/service/hash/{hash_key}/status",
        )


class DeepSignBackend(SignatureBackend):
    """Hash signing via the DeepSign API, confirmed in the DeepID app.

    Credentials are stored per group in `DeepSignServiceAccount`, delivered
    by DeepSign through the connection callback.
    """

    SIGNATURE_TYPES = {
        "timestamp": Signature.Type.TIMESTAMP,
        "advanced": Signature.Type.ADVANCED,
        "qualified": Signature.Type.QUALIFIED,
    }

    def is_enabled_for(self, group):
        return DeepSignServiceAccount.objects.connected().for_group(group).exists()

    def _get_client(self, group) -> DeepSignClient:
        account = DeepSignServiceAccount.objects.connected().for_group(group).get()
        return DeepSignClient(account)

    def request_signature(self, signature_request):
        signature_request.signature_type = self.SIGNATURE_TYPES[
            settings.ALEXANDRIA_DEEPSIGN_SIGNATURE_MODE
        ]
        client = self._get_client(signature_request.created_by_group)

        person = client.register_person(
            f"{settings.ALEXANDRIA_DEEPSIGN_PERSON_REF_PREFIX}"
            f"{signature_request.created_by_user}"
        )
        if person.get("registrationDeepLink"):
            signature_request.status = SignatureRequest.Status.REGISTRATION_REQUIRED
            signature_request.action_url = person["registrationDeepLink"]
            return
        if not person.get("personIdentityUid"):
            log.error("Unexpected DeepSign registration response: %s", person)
            raise SignatureProviderError()

        file = signature_request.file
        with file.content.open() as content:
            prepared = pdf.prepare(
                content.read(),
                bytes_reserved=settings.ALEXANDRIA_DEEPSIGN_SIGNATURE_BYTES_RESERVED,
            )

        result = client.sign_hash(
            hash_id=str(signature_request.pk),
            digest=prepared.digest.document_digest,
            document_name=file.name,
            signature_mode=settings.ALEXANDRIA_DEEPSIGN_SIGNATURE_MODE,
            identity_uid=person["personIdentityUid"],
        )
        if not result.get("hashKey"):
            log.error("Unexpected DeepSign sign response: %s", result)
            raise SignatureProviderError()

        signature_request.status = SignatureRequest.Status.REQUESTED
        signature_request.provider_reference = result["hashKey"]
        signature_request.provider_data = {
            "digest": pdf.serialize_digest(prepared.digest)
        }
        signature_request.prepared_content = prepared.content
        signature_request.timeout = timezone.now() + timedelta(
            seconds=settings.ALEXANDRIA_DEEPSIGN_TIMEOUT_SECONDS
        )
        # Timestamps (stamps) are signed without confirmation
        self._apply_status(signature_request, result)

    def poll_signature(self, signature_request):
        client = self._get_client(signature_request.created_by_group)
        self._apply_status(
            signature_request, client.get_status(signature_request.provider_reference)
        )

        if signature_request.is_active and timezone.now() > signature_request.timeout:
            self._end(signature_request, SignatureRequest.Status.TIMEOUT)

    def cancel_signature(self, signature_request):
        if signature_request.provider_reference:
            # Fetch the final state, the user may have confirmed in the meantime
            client = self._get_client(signature_request.created_by_group)
            self._apply_status(
                signature_request,
                client.get_status(signature_request.provider_reference),
            )

        if signature_request.is_active:
            self._end(signature_request, SignatureRequest.Status.TIMEOUT)

    def _apply_status(self, signature_request, result):
        status = result.get("signStatus")
        signature_request.provider_status = status

        if status == DeepSignClient.STATUS_SIGNED:
            self._finish(signature_request, result)
        elif status == DeepSignClient.STATUS_REJECTED:
            self._end(signature_request, SignatureRequest.Status.REJECTED)

    def stamp(self, file, user, group, data):
        """Add the visible stamp (optional) and a DeepSign timestamp.

        `data` may contain `image` (PNG/JPEG bytes) and `text` (e.g. the
        decision date), shown as appearance of the timestamp field at
        `ALEXANDRIA_DEEPSIGN_STAMP_BOX`, so the timestamp covers it. Missing
        values are taken from `ALEXANDRIA_DEEPSIGN_STAMP_DATA_FUNCTION`.
        """
        client = self._get_client(group)
        results = []
        if settings.ALEXANDRIA_DEEPSIGN_STAMP_DATA_FUNCTION:
            # e.g. the stamp image of the municipality, explicit data wins
            get_data = import_string(settings.ALEXANDRIA_DEEPSIGN_STAMP_DATA_FUNCTION)
            data = {**get_data(file=file, user=user, group=group), **data}

        def request_token(digest: bytes) -> bytes:
            result = client.sign_hash(
                hash_id=str(uuid.uuid4()),
                digest=digest,
                document_name=file.name,
                signature_mode=DeepSignClient.MODE_TIMESTAMP,
            )
            hash_key = result.get("hashKey")
            for _attempt in range(STAMP_STATUS_ATTEMPTS):
                if result.get("signStatus") != DeepSignClient.STATUS_IN_PROGRESS:
                    break
                if not hash_key:
                    log.error("Unexpected DeepSign stamp response: %s", result)
                    raise SignatureProviderError()
                time.sleep(STAMP_STATUS_INTERVAL_SECONDS)
                result = client.get_status(hash_key)

            if result.get("signStatus") != DeepSignClient.STATUS_SIGNED:
                log.error("DeepSign did not return the stamp: %s", result)
                raise SignatureProviderError()

            results.append(result)
            # RFC 3161 timestamp token, not a CMS signature
            return self._extract_signature(result)

        with file.content.open() as content:
            stamped = content.read()

        appearance = None
        if data.get("image") or data.get("text"):
            appearance = pdf.StampAppearance(
                box=tuple(settings.ALEXANDRIA_DEEPSIGN_STAMP_BOX),
                image=data.get("image"),
                text=data.get("text"),
                page=settings.ALEXANDRIA_DEEPSIGN_STAMP_PAGE,
                opacity=settings.ALEXANDRIA_DEEPSIGN_STAMP_OPACITY,
            )

        stamped = pdf.timestamp(
            stamped,
            bytes_reserved=settings.ALEXANDRIA_DEEPSIGN_SIGNATURE_BYTES_RESERVED,
            request_token=request_token,
            appearance=appearance,
        )
        token = self._extract_signature(results[-1])
        stamped = pdf.add_validation_info(
            stamped, **self._validation_info(results[-1], token)
        )

        return store_signed_file(
            file,
            content=stamped,
            signature=token,
            signature_type=Signature.Type.TIMESTAMP,
            user=user,
            group=group,
        )

    def _validation_info(self, result, token: bytes) -> dict:
        """Return certificates and revocation info for long-term validation.

        DeepSign returns the revocation info (`crls`, `ocsps`, base64 DER)
        next to the signatures, the certificates are part of the token.
        """
        signature_data = result.get("signatureData") or {}
        try:
            return {
                "certs": pdf.timestamp_certificates(token),
                "ocsps": [
                    base64.b64decode(o) for o in signature_data.get("ocsps") or []
                ],
                "crls": [base64.b64decode(c) for c in signature_data.get("crls") or []],
            }
        except (TypeError, ValueError) as e:
            log.exception("DeepSign returned invalid revocation info: %s", result)
            raise SignatureProviderError() from e

    def _extract_signature(self, result) -> bytes:
        try:
            return base64.b64decode(
                result["signatureData"]["signatures"][0]["signature"]
            )
        except (KeyError, IndexError, TypeError, ValueError) as e:
            log.exception("DeepSign returned no signature: %s", result)
            raise SignatureProviderError() from e

    def _finish(self, signature_request, result):
        signature = self._extract_signature(result)
        content = pdf.finish(
            signature_request.prepared_content,
            pdf.deserialize_digest(signature_request.provider_data["digest"]),
            signature,
        )
        store_signed_file(
            signature_request.file,
            content=content,
            signature=signature,
            signature_type=signature_request.signature_type,
            user=signature_request.created_by_user,
            group=signature_request.created_by_group,
            signature_request=signature_request,
        )

    def _end(self, signature_request, status):
        signature_request.status = status
        signature_request.prepared_content = None

import hashlib
from typing import Optional, Tuple

from django.conf import settings
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from rest_framework.exceptions import ValidationError
from rest_framework_json_api.relations import reverse


def make_signature_components(
    pk: str,
    hostname: str,
    expires: Optional[int] = None,
    scheme: str = "http",
    download_path: Optional[str] = None,
) -> Tuple[str, int, str]:
    """Make the components used to sign and verify the download_url.

    If `expires` is provided the components are called for the verification step.

    Otherwise expiry is calculated and returned
    """
    if not expires:
        expires = int(
            (
                timezone.now()
                + timezone.timedelta(seconds=settings.ALEXANDRIA_DOWNLOAD_URL_LIFETIME)
            ).timestamp()
        )
    download_path = download_path or reverse("file-download", args=[pk])
    host = f"{scheme}://{hostname}"
    url = f"{host.strip('/')}{download_path}"
    token = f"{url}{expires}{settings.SECRET_KEY}"
    hash = hashlib.shake_256(token.encode())
    # Django's base64 encoder strips padding and ascii-decodes the output
    signature = urlsafe_base64_encode(hash.digest(32))
    return url, expires, signature


def verify_signed_components(
    pk: str,
    hostname: str,
    token_sig: str,
    expires: Optional[int],
    scheme: str = "http",
    download_path: Optional[str] = None,
):
    """Verify a presigned download URL.

    It tests against the expiry: raises a TimeoutError
    It tests against signature integrity: raises an AssertionError

    returns True otherwise.
    """
    now = timezone.now()
    host, expires, signature = make_signature_components(
        pk, hostname, expires, scheme, download_path
    )

    if int(now.timestamp()) > expires:
        raise ValidationError("Download URL expired.")
    if not token_sig == signature:
        raise ValidationError("Invalid signature.")

    return True

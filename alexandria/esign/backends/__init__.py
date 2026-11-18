from django.conf import settings
from django.utils.module_loading import import_string

from .base import SignatureBackend


def get_backend() -> SignatureBackend | None:
    """Return the signature backend configured for this deployment.

    `None` if signing is not enabled (`ALEXANDRIA_ESIGN_BACKEND` not set).
    Existing signatures are still shown.
    """
    if not settings.ALEXANDRIA_ESIGN_BACKEND:
        return None
    return import_string(settings.ALEXANDRIA_ESIGN_BACKEND)()

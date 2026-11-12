from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models


def _fernet() -> Fernet:
    key = settings.ALEXANDRIA_ESIGN_ENCRYPTION_KEY
    if not key:
        raise ImproperlyConfigured(
            "`ALEXANDRIA_ESIGN_ENCRYPTION_KEY` is required to store credentials"
        )
    return Fernet(key)


def encrypt(value: str) -> str:
    return _fernet().encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    try:
        return _fernet().decrypt(value.encode()).decode()
    except InvalidToken as e:
        raise ImproperlyConfigured(
            "Stored credentials can't be decrypted, was "
            "`ALEXANDRIA_ESIGN_ENCRYPTION_KEY` changed?"
        ) from e


class EncryptedTextField(models.TextField):
    """Text encrypted at rest with Fernet (AES-128-CBC with HMAC).

    Empty values are stored as is. Filtering on the field does not work, the
    stored value differs on every save.
    """

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return encrypt(value) if value else value

    def from_db_value(self, value, expression, connection):
        return decrypt(value) if value else value

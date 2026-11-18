import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db import connection

from alexandria.esign.models import DeepSignServiceAccount


@pytest.mark.django_db
def test_password_encrypted_at_rest(deep_sign_service_account_factory):
    account = deep_sign_service_account_factory(password="secret")

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT password FROM alexandria_esign_deepsignserviceaccount "
            "WHERE id = %s",
            [account.pk],
        )
        (stored,) = cursor.fetchone()

    assert stored != "secret"
    assert DeepSignServiceAccount.objects.get(pk=account.pk).password == "secret"


@pytest.mark.django_db
def test_password_requires_key(settings, deep_sign_service_account_factory):
    settings.ALEXANDRIA_ESIGN_ENCRYPTION_KEY = None

    with pytest.raises(ImproperlyConfigured):
        deep_sign_service_account_factory(password="secret")


@pytest.mark.django_db
def test_password_wrong_key(settings, deep_sign_service_account_factory):
    account = deep_sign_service_account_factory(password="secret")
    settings.ALEXANDRIA_ESIGN_ENCRYPTION_KEY = (
        "Y6ARqJXoX8dO2RiGFBIWaFLX_UlFzQFCg_fmv1F3_Ww="
    )

    with pytest.raises(ImproperlyConfigured):
        DeepSignServiceAccount.objects.get(pk=account.pk)

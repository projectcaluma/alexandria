import json
from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from alexandria.esign.backends.deepsign import DeepSignBackend
from alexandria.esign.models import DeepSignServiceAccount


@pytest.fixture
def deepsign_settings(settings):
    settings.ALEXANDRIA_DEEPSIGN_PARTNER_CLIENT_ID = "partner-client"
    settings.ALEXANDRIA_DEEPSIGN_CALLBACK_URL = (
        "https://alexandria.example.com/api/v1/deepsign/callback"
    )
    settings.ALEXANDRIA_DEEPSIGN_CALLBACK_REDIRECT_URL = "https://ebau.example.com/"
    return settings


@pytest.mark.django_db
@pytest.mark.parametrize(
    "account_kwargs,expected",
    [
        ({"group": "admin"}, True),
        ({"group": "admin", "connected_at": None}, False),
        ({"group": "other"}, False),
    ],
)
def test_is_enabled_for(deep_sign_service_account_factory, account_kwargs, expected):
    deep_sign_service_account_factory(**account_kwargs)

    assert DeepSignBackend().is_enabled_for("admin") is expected


@pytest.mark.django_db
def test_start_connection(admin_client, deepsign_settings):
    response = admin_client.post(
        reverse("deepsignserviceaccount-list"),
        {"data": {"type": "deepsign-service-accounts", "attributes": {}}},
    )

    assert response.status_code == HTTP_201_CREATED, response.json()
    account = DeepSignServiceAccount.objects.get()
    assert account.group == "admin"
    assert account.connected_at is None

    url = urlparse(response.json()["data"]["attributes"]["connection-url"])
    params = parse_qs(url.query)
    assert params["client_id"] == ["partner-client"]
    assert params["redirect_uri"] == [
        deepsign_settings.ALEXANDRIA_DEEPSIGN_CALLBACK_URL
    ]
    assert json.loads(params["state"][0]) == {
        "group": "admin",
        "token": account.state_token,
    }


@pytest.mark.django_db
def test_restart_connection_rotates_token(
    admin_client, deepsign_settings, deep_sign_service_account
):
    old_token = deep_sign_service_account.state_token

    response = admin_client.post(
        reverse("deepsignserviceaccount-list"),
        {"data": {"type": "deepsign-service-accounts", "attributes": {}}},
    )

    assert response.status_code == HTTP_201_CREATED, response.json()
    deep_sign_service_account.refresh_from_db()
    assert deep_sign_service_account.state_token != old_token
    assert DeepSignServiceAccount.objects.count() == 1


@pytest.mark.django_db
def test_list_only_own_group(admin_client, deep_sign_service_account_factory):
    own = deep_sign_service_account_factory(group="admin")
    deep_sign_service_account_factory(group="other")

    response = admin_client.get(reverse("deepsignserviceaccount-list"))

    assert response.status_code == HTTP_200_OK
    assert [a["id"] for a in response.json()["data"]] == [str(own.pk)]


def _callback_data(account, **overrides):
    return {
        "state": json.dumps({"group": account.group, "token": account.state_token}),
        "service_account_id": "account-id",
        "service_account_username": "service-user",
        "service_account_password": "secret",
        "creator_email": "creator@example.com",
        "creator_language": "de",
        **overrides,
    }


@pytest.mark.django_db
def test_callback_stores_credentials(
    client, deepsign_settings, deep_sign_service_account_factory
):
    account = deep_sign_service_account_factory(
        account_id="", username="", password="", connected_at=None
    )
    old_token = account.state_token

    response = client.post(
        reverse("deepsign-callback"), _callback_data(account), format="multipart"
    )

    assert response.status_code == 302
    assert response["Location"] == "https://ebau.example.com/"
    account.refresh_from_db()
    assert account.account_id == "account-id"
    assert account.username == "service-user"
    assert account.password == "secret"
    assert account.connected_at is not None
    assert account.state_token != old_token


@pytest.mark.django_db
@pytest.mark.parametrize(
    "make_overrides",
    [
        lambda account: {"state": json.dumps({"group": "admin", "token": "wrong"})},
        lambda account: {
            "state": json.dumps({"group": "other", "token": account.state_token})
        },
        lambda account: {"state": "no json"},
        lambda account: {"state": "[]"},
        lambda account: {"service_account_password": None},
    ],
)
def test_callback_rejects_invalid_request(
    client, deep_sign_service_account_factory, make_overrides
):
    account = deep_sign_service_account_factory(connected_at=None)
    data = {
        key: value
        for key, value in _callback_data(account, **make_overrides(account)).items()
        if value is not None
    }

    response = client.post(reverse("deepsign-callback"), data, format="multipart")

    assert response.status_code == 400
    account.refresh_from_db()
    assert account.connected_at is None

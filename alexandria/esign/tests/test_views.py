import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from alexandria.core.models import File
from alexandria.esign.api import stamp_file
from alexandria.esign.models import Signature, SignatureRequest
from alexandria.esign.tests.backends import FakeBackend


def _post_data(file):
    return {
        "data": {
            "type": "signature-requests",
            "relationships": {"file": {"data": {"type": "files", "id": str(file.pk)}}},
        }
    }


@pytest.mark.django_db
def test_create_signature_request(admin_client, file_factory):
    file = file_factory(mime_type="application/pdf")

    response = admin_client.post(reverse("signaturerequest-list"), _post_data(file))

    assert response.status_code == HTTP_201_CREATED, response.json()
    attributes = response.json()["data"]["attributes"]
    assert attributes["status"] == SignatureRequest.Status.REQUESTED
    assert attributes["action-url"] == "https://signing.example.com/fake-ref"

    request = SignatureRequest.objects.get()
    assert request.file == file
    assert request.provider_reference == "fake-ref"
    assert request.created_by_user == "admin"


@pytest.mark.django_db
def test_create_returns_own_active_request(admin_client, signature_request_factory):
    existing = signature_request_factory(created_by_user="admin")

    response = admin_client.post(
        reverse("signaturerequest-list"), _post_data(existing.file)
    )

    assert response.status_code == HTTP_200_OK, response.json()
    assert response.json()["data"]["id"] == str(existing.pk)
    assert SignatureRequest.objects.count() == 1


@pytest.mark.django_db
def test_create_rejects_active_request_of_other_user(
    admin_client, signature_request_factory
):
    existing = signature_request_factory(created_by_user="someone-else")

    response = admin_client.post(
        reverse("signaturerequest-list"), _post_data(existing.file)
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert SignatureRequest.objects.count() == 1


@pytest.mark.django_db
def test_create_allowed_after_finished_request(admin_client, signature_request_factory):
    finished = signature_request_factory(
        created_by_user="someone-else", status=SignatureRequest.Status.TIMEOUT
    )

    response = admin_client.post(
        reverse("signaturerequest-list"), _post_data(finished.file)
    )

    assert response.status_code == HTTP_201_CREATED
    assert SignatureRequest.objects.count() == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    "file_kwargs",
    [
        {"mime_type": "image/png"},
        {"variant": File.Variant.THUMBNAIL, "mime_type": "application/pdf"},
    ],
)
def test_create_rejects_invalid_file(admin_client, file_factory, file_kwargs):
    file = file_factory(**file_kwargs)

    response = admin_client.post(reverse("signaturerequest-list"), _post_data(file))

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert not SignatureRequest.objects.exists()


@pytest.mark.django_db
def test_create_requires_enabled_group(admin_client, file_factory, mocker):
    mocker.patch.object(FakeBackend, "enabled_groups", set())
    file = file_factory(mime_type="application/pdf")

    response = admin_client.post(reverse("signaturerequest-list"), _post_data(file))

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert not SignatureRequest.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "status,expected_status",
    [
        (SignatureRequest.Status.REQUESTED, SignatureRequest.Status.DONE),
        (SignatureRequest.Status.REJECTED, SignatureRequest.Status.REJECTED),
    ],
)
def test_retrieve_polls_active_request(
    admin_client, signature_request_factory, status, expected_status
):
    signature_request = signature_request_factory(status=status)

    response = admin_client.get(
        reverse("signaturerequest-detail", args=[signature_request.pk])
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["data"]["attributes"]["status"] == expected_status
    signature_request.refresh_from_db()
    assert signature_request.status == expected_status


@pytest.mark.django_db
def test_signature_list_filter_by_file(admin_client, signature_factory):
    signature = signature_factory()
    signature_factory()

    response = admin_client.get(
        reverse("signature-list"),
        {"filter[file]": str(signature.file.pk), "include": "file"},
    )

    assert response.status_code == HTTP_200_OK, response.json()
    data = response.json()["data"]
    assert [s["id"] for s in data] == [str(signature.pk)]
    assert data[0]["attributes"]["signature-type"] == "qualified"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_name", ["signaturerequest-list", "deepsignserviceaccount-list"]
)
def test_signing_requires_authentication(client, settings, url_name):
    # Anonymous write is enabled in development, signing needs a user anyway
    settings.REST_FRAMEWORK = {
        **settings.REST_FRAMEWORK,
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    }

    response = client.post(reverse(url_name), {})

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_create_ignores_client_group(admin_client, file_factory):
    file = file_factory(mime_type="application/pdf")
    data = _post_data(file)
    data["data"]["attributes"] = {"created-by-group": "other"}

    response = admin_client.post(reverse("signaturerequest-list"), data)

    assert response.status_code == HTTP_201_CREATED, response.json()
    assert SignatureRequest.objects.get().created_by_group == "admin"


def _stamp_data(file):
    return {
        "data": {
            "type": "signatures",
            "relationships": {"file": {"data": {"type": "files", "id": str(file.pk)}}},
        }
    }


@pytest.mark.django_db
def test_stamp(admin_client, file_factory):
    file = file_factory(mime_type="application/pdf")

    response = admin_client.post(reverse("signature-list"), _stamp_data(file))

    assert response.status_code == HTTP_201_CREATED, response.json()
    assert response.json()["data"]["attributes"]["signature-type"] == "timestamp"
    signature = Signature.objects.get()
    assert signature.created_by_user == "admin"
    assert signature.created_by_group == "admin"
    # Recorded as finished request, so it shows up in the history
    request = signature.signature_request
    assert request.file == file
    assert request.signature_type == SignatureRequest.Type.TIMESTAMP
    assert request.status == SignatureRequest.Status.DONE
    assert request.created_by_user == "admin"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "group,file_kwargs",
    [
        ("other", {"mime_type": "application/pdf"}),
        ("admin", {"mime_type": "text/plain"}),
    ],
)
def test_stamp_rejected(admin_client, admin_user, file_factory, group, file_kwargs):
    admin_user.group = group
    file = file_factory(**file_kwargs)

    response = admin_client.post(reverse("signature-list"), _stamp_data(file))

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert not Signature.objects.exists()


@pytest.mark.django_db
def test_filter_signature_requests_by_document(
    admin_client, signature_request_factory, file_factory
):
    own = signature_request_factory()
    newer_version = file_factory(document=own.file.document)
    on_newer_version = signature_request_factory(file=newer_version)
    signature_request_factory()

    response = admin_client.get(
        reverse("signaturerequest-list"),
        {"filter[document]": str(own.file.document.pk)},
    )

    assert response.status_code == HTTP_200_OK
    assert {r["id"] for r in response.json()["data"]} == {
        str(own.pk),
        str(on_newer_version.pk),
    }


@pytest.mark.django_db
def test_stamp_request_type_from_backend(admin_client, file_factory, mocker):
    # e.g. a provider creating qualified seals
    mocker.patch(
        "alexandria.esign.tests.backends.FakeBackend.stamp_type",
        Signature.Type.QUALIFIED,
    )
    file = file_factory(mime_type="application/pdf")

    response = admin_client.post(reverse("signature-list"), _stamp_data(file))

    assert response.status_code == HTTP_201_CREATED, response.json()
    assert (
        Signature.objects.get().signature_request.signature_type
        == Signature.Type.QUALIFIED
    )


@pytest.mark.django_db
def test_signing_disabled(settings, admin_client, file_factory):
    settings.ALEXANDRIA_ESIGN_BACKEND = None
    file = file_factory(mime_type="application/pdf")

    response = admin_client.post(reverse("signaturerequest-list"), _post_data(file))
    document = admin_client.get(reverse("document-detail", args=[file.document.pk]))

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert document.json()["data"]["attributes"]["can-sign"] is False
    with pytest.raises(ImproperlyConfigured):
        stamp_file(file, user="admin", group="admin")


@pytest.mark.django_db
def test_poll_signing_disabled(settings, admin_client, signature_request_factory):
    signature_request = signature_request_factory(created_by_user="admin")
    settings.ALEXANDRIA_ESIGN_BACKEND = None

    response = admin_client.get(
        reverse("signaturerequest-detail", args=[signature_request.pk])
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["data"]["attributes"]["status"] == "open"

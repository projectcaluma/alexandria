import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from alexandria.core.models import File
from alexandria.esign.models import SignatureRequest


def _post_data(file):
    return {
        "data": {
            "type": "signature-requests",
            "relationships": {"file": {"data": {"type": "files", "id": str(file.pk)}}},
        }
    }


@pytest.mark.django_db
def test_create_signature_request(
    admin_client, file_factory, signature_provider_credentials
):
    file = file_factory(mime_type="application/pdf")

    response = admin_client.post(reverse("signaturerequest-list"), _post_data(file))

    assert response.status_code == HTTP_201_CREATED, response.json()
    request = SignatureRequest.objects.get()
    assert request.file == file
    assert request.status == SignatureRequest.Status.OPEN
    assert request.created_by_user == "admin"


@pytest.mark.django_db
def test_create_returns_own_active_request(
    admin_client, signature_request_factory, signature_provider_credentials
):
    existing = signature_request_factory(created_by_user="admin")

    response = admin_client.post(
        reverse("signaturerequest-list"), _post_data(existing.file)
    )

    assert response.status_code == HTTP_200_OK, response.json()
    assert response.json()["data"]["id"] == str(existing.pk)
    assert SignatureRequest.objects.count() == 1


@pytest.mark.django_db
def test_create_rejects_active_request_of_other_user(
    admin_client, signature_request_factory, signature_provider_credentials
):
    existing = signature_request_factory(created_by_user="someone-else")

    response = admin_client.post(
        reverse("signaturerequest-list"), _post_data(existing.file)
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert SignatureRequest.objects.count() == 1


@pytest.mark.django_db
def test_create_allowed_after_finished_request(
    admin_client, signature_request_factory, signature_provider_credentials
):
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
def test_create_rejects_invalid_file(
    admin_client, file_factory, signature_provider_credentials, file_kwargs
):
    file = file_factory(**file_kwargs)

    response = admin_client.post(reverse("signaturerequest-list"), _post_data(file))

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert not SignatureRequest.objects.exists()


@pytest.mark.django_db
def test_create_requires_provider_credentials(admin_client, file_factory):
    file = file_factory(mime_type="application/pdf")

    response = admin_client.post(reverse("signaturerequest-list"), _post_data(file))

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert not SignatureRequest.objects.exists()


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

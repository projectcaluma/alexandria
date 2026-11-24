from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from alexandria.esign import api
from alexandria.esign.models import SignatureRequest


def _request_data(file):
    return {
        "data": {
            "type": "signature-requests",
            "relationships": {"file": {"data": {"type": "files", "id": str(file.pk)}}},
        }
    }


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_name,data_type",
    [
        ("signaturerequest-list", "signature-requests"),
        ("signature-list", "signatures"),
    ],
)
def test_only_latest_version(
    admin_client, document_factory, file_factory, url_name, data_type
):
    document = document_factory()
    old = file_factory(document=document, mime_type="application/pdf")
    file_factory(document=document, mime_type="application/pdf")
    data = _request_data(old)
    data["data"]["type"] = data_type

    response = admin_client.post(reverse(url_name), data)

    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_store_outdated_file(document_factory, file_factory):
    document = document_factory()
    old = file_factory(document=document, mime_type="application/pdf")
    file_factory(document=document, mime_type="application/pdf")

    with pytest.raises(api.OutdatedFileError):
        api.store_signed_file(
            old, b"%PDF", b"sig", "qualified", user="admin", group="admin"
        )


@pytest.mark.django_db
def test_poll_outdated(admin_client, signature_request_factory, file_factory):
    signature_request = signature_request_factory(
        created_by_user="admin", status=SignatureRequest.Status.REQUESTED
    )
    # New version while waiting for the confirmation
    file_factory(document=signature_request.file.document)

    response = admin_client.get(
        reverse("signaturerequest-detail", args=[signature_request.pk])
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["data"]["attributes"]["status"] == "outdated"


@pytest.mark.django_db
def test_expired_request_does_not_block(
    admin_client, signature_request_factory, file_factory
):
    file = file_factory(mime_type="application/pdf")
    expired = signature_request_factory(
        file=file,
        created_by_user="someone-else",
        status=SignatureRequest.Status.REQUESTED,
        timeout=timezone.now() - timedelta(minutes=1),
    )

    response = admin_client.post(reverse("signaturerequest-list"), _request_data(file))

    assert response.status_code == HTTP_201_CREATED, response.json()
    expired.refresh_from_db()
    assert expired.status == SignatureRequest.Status.TIMEOUT

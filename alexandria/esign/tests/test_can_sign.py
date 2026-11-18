import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from alexandria.core.models import File


@pytest.mark.django_db
@pytest.mark.parametrize(
    "group,latest_mime_type,expected",
    [
        ("admin", "application/pdf", True),
        ("other", "application/pdf", False),
        ("admin", "text/plain", False),
    ],
)
def test_document_can_sign(
    admin_client,
    admin_user,
    document_factory,
    file_factory,
    group,
    latest_mime_type,
    expected,
):
    admin_user.group = group
    document = document_factory()
    file_factory(document=document, mime_type="text/plain")
    latest = file_factory(document=document, mime_type=latest_mime_type)
    # Renderings are ignored
    file_factory(
        document=document,
        original=latest,
        variant=File.Variant.THUMBNAIL,
        mime_type="image/jpeg",
    )

    response = admin_client.get(reverse("document-detail", args=[document.pk]))

    assert response.status_code == HTTP_200_OK
    assert response.json()["data"]["attributes"]["can-sign"] is expected


@pytest.mark.django_db
def test_document_without_files_cannot_be_signed(admin_client, document_factory):
    document = document_factory()

    response = admin_client.get(reverse("document-detail", args=[document.pk]))

    assert response.json()["data"]["attributes"]["can-sign"] is False

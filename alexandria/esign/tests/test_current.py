import pytest
from django.urls import reverse
from generic_permissions.config import ObjectPermissionsConfig
from generic_permissions.permissions import object_permission_for
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from alexandria.core.models import Document
from alexandria.esign import api
from alexandria.esign.models import Signature, SignatureRequest


@pytest.fixture
def signed_document(document_factory, file_factory, signature_request_factory):
    """Upload, QES signature, then stamp: every version still current."""
    document = document_factory()
    upload = file_factory(document=document, mime_type="application/pdf")
    sign_request = signature_request_factory(
        file=upload,
        status=SignatureRequest.Status.DONE,
        signature_type=SignatureRequest.Type.QUALIFIED,
    )
    signed = file_factory(document=document, mime_type="application/pdf")
    Signature.objects.create(
        file=signed,
        signature_request=sign_request,
        signature_type=Signature.Type.QUALIFIED,
        signer_name="Winston Smith",
        signed_at=signed.created_at,
        signature_hash="hash",
    )
    stamp_request = signature_request_factory(
        file=signed,
        status=SignatureRequest.Status.DONE,
        signature_type=SignatureRequest.Type.TIMESTAMP,
    )
    stamped = file_factory(document=document, mime_type="application/pdf")
    Signature.objects.create(
        file=stamped,
        signature_request=stamp_request,
        signature_type=Signature.Type.TIMESTAMP,
        signer_name="TSA",
        signed_at=stamped.created_at,
        signature_hash="hash",
    )
    return document


def _document_attributes(client, document):
    response = client.get(reverse("document-detail", args=[document.pk]))
    assert response.status_code == HTTP_200_OK
    return response.json()["data"]["attributes"]


def _current_flags(client, document):
    response = client.get(
        reverse("signaturerequest-list"), {"filter[document]": str(document.pk)}
    )
    assert response.status_code == HTTP_200_OK
    return {
        r["attributes"]["signature-type"]: r["attributes"]["is-current"]
        for r in response.json()["data"]
    }


@pytest.mark.django_db
def test_signatures_current(admin_client, signed_document):
    assert len(api.current_files(signed_document)) == 3

    attributes = _document_attributes(admin_client, signed_document)
    assert attributes["is-signed"] is True
    assert attributes["is-stamped"] is True
    assert _current_flags(admin_client, signed_document) == {
        "qualified": True,
        "timestamp": True,
    }


@pytest.mark.django_db
def test_new_version_invalidates_signatures(
    admin_client, signed_document, file_factory
):
    # e.g. replaced or edited via WebDAV
    file_factory(document=signed_document, mime_type="application/pdf")

    assert len(api.current_files(signed_document)) == 1

    attributes = _document_attributes(admin_client, signed_document)
    assert attributes["is-signed"] is False
    assert attributes["is-stamped"] is False
    assert _current_flags(admin_client, signed_document) == {
        "qualified": False,
        "timestamp": False,
    }


@pytest.mark.django_db
def test_signer_name_and_signed_file(admin_client, signed_document):
    response = admin_client.get(
        reverse("signaturerequest-list"),
        {
            "filter[document]": str(signed_document.pk),
            "filter[signature_type]": "qualified",
        },
    )

    data = response.json()["data"][0]
    signature = Signature.objects.get(signature_type=Signature.Type.QUALIFIED)
    assert data["attributes"]["signer-name"] == "Winston Smith"
    # The version created by the signature, the request was made on the previous
    assert data["relationships"]["signed-file"]["data"]["id"] == str(signature.file.pk)
    assert data["relationships"]["file"]["data"]["id"] != str(signature.file.pk)


class DenyAction:
    denied = ""

    @object_permission_for(Document)
    def has_object_permission_for_document(self, request, instance, action=None):
        return action != self.denied


@pytest.mark.django_db
@pytest.mark.parametrize(
    "denied,url_name,data_type",
    [
        ("sign", "signaturerequest-list", "signature-requests"),
        ("stamp", "signature-list", "signatures"),
    ],
)
def test_document_permission(
    admin_client, file_factory, reset_config_classes, denied, url_name, data_type
):
    DenyAction.denied = denied
    ObjectPermissionsConfig.register_handler_class(DenyAction)
    file = file_factory(mime_type="application/pdf")

    response = admin_client.post(
        reverse(url_name),
        {
            "data": {
                "type": data_type,
                "relationships": {
                    "file": {"data": {"type": "files", "id": str(file.pk)}}
                },
            }
        },
    )

    assert response.status_code == HTTP_403_FORBIDDEN
    assert _document_attributes(admin_client, file.document)["can-sign"] is (
        denied != "sign"
    )

from io import BytesIO

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from pyhanko.pdf_utils.reader import PdfFileReader

from alexandria.esign.backends.local import LocalBackend
from alexandria.esign.dev import example_stamp_data
from alexandria.esign.models import Signature, SignatureRequest


@pytest.fixture
def pdf_file(settings, file_factory, pdf_content):
    settings.DEBUG = True
    return file_factory(
        name="decision.pdf",
        mime_type="application/pdf",
        content=ContentFile(pdf_content, name="decision.pdf"),
    )


def test_requires_debug(settings):
    settings.DEBUG = False

    with pytest.raises(ImproperlyConfigured):
        LocalBackend()


@pytest.mark.django_db
def test_sign(pdf_file, signature_request_factory):
    signature_request = signature_request_factory(
        file=pdf_file, created_by_user="admin", created_by_group="admin"
    )
    backend = LocalBackend()

    assert backend.is_enabled_for("admin")
    backend.request_signature(signature_request)
    assert signature_request.status == SignatureRequest.Status.REQUESTED
    backend.poll_signature(signature_request)

    assert signature_request.status == SignatureRequest.Status.DONE
    signature = Signature.objects.get()
    assert signature.signer_name == "Alexandria Development"
    assert signature.signature_type == Signature.Type.ADVANCED


@pytest.mark.django_db
def test_cancel(pdf_file, signature_request_factory):
    signature_request = signature_request_factory(file=pdf_file)
    backend = LocalBackend()
    backend.request_signature(signature_request)

    backend.cancel_signature(signature_request)

    assert signature_request.status == SignatureRequest.Status.TIMEOUT
    assert signature_request.prepared_content is None


@pytest.mark.django_db
@pytest.mark.parametrize("visible", [True, False])
def test_stamp(pdf_file, visible):
    data = example_stamp_data(pdf_file, "admin", "admin") if visible else {}

    result = LocalBackend().stamp(pdf_file, user="admin", group="admin", data=data)

    stamp = PdfFileReader(BytesIO(result.file.content.read())).embedded_signatures[-1]
    assert stamp.sig_object_type == "/DocTimeStamp"
    assert any(float(v) for v in stamp.sig_field["/Rect"]) is visible

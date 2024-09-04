import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError

from alexandria.core import api
from alexandria.core.factories import FileData


def test_create_document_file(db, category):
    doc, file = api.create_document_file(
        "Foo",
        "Baz",
        category,
        "Bar.pdf",
        "Mee.pdf",
        SimpleUploadedFile(
            name="test.png",
            content=FileData.png,
            content_type="png",
        ),
        "image/png",
        1,
    )
    assert doc.title == "Bar.pdf"
    assert file.name == "Mee.pdf"


def test_presigning_api(db, file):
    _, expires, signature = api.make_signature_components(
        file.pk, "testserver", download_path="/foo"
    )

    api.verify_signed_components(
        file.pk, "testserver", signature, expires, download_path="/foo"
    )
    with pytest.raises(ValidationError):
        api.verify_signed_components(
            file.pk, "testserver", "incorrect-signature", expires, download_path="/foo"
        )

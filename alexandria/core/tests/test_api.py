from django.core.files.uploadedfile import SimpleUploadedFile

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


def test_presigning_api(mocker):
    mock = mocker.patch("alexandria.core.presign_urls.make_signature_components")
    api.make_signature_components("123", "foo")
    mock.assert_called_once_with("123", "foo", None, "http", None)

    mock = mocker.patch("alexandria.core.presign_urls.verify_signed_components")
    api.verify_signed_components("123", "foo", "foo", "http", "abcabc")
    mock.assert_called_once_with("123", "foo", "foo", "http", "abcabc")

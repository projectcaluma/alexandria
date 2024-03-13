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

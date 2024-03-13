from django.core.files.uploadedfile import SimpleUploadedFile

from alexandria.core import utils
from alexandria.core.factories import FileData


def test_create_document_file(db, category):
    doc, file = utils.create_document_file(
        "Foo",
        "Baz",
        {"title": "Bar.pdf", "category": category},
        {
            "name": "Bar.pdf",
            "content": SimpleUploadedFile(
                name="test.png",
                content=FileData.png,
                content_type="png",
            ),
            "mime_type": "image/png",
            "size": 1,
        },
    )
    assert doc.title == "Bar.pdf"
    assert file.name == "Bar.pdf"

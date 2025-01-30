import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from alexandria.core import api
from alexandria.core.factories import FileData
from alexandria.core.models import File


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


@pytest.mark.parametrize(
    "same_category",
    [
        True,
        False,
    ],
)
def test_copy_document_api(db, category, category_factory, same_category):
    # initial document with one file
    input_doc, first_file = api.create_document_file(
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

    # add an extra file to the document
    extra_file = api.create_file(
        input_doc,
        "Foo2",
        "Baz2",
        "Mee2.pdf",
        SimpleUploadedFile(
            name="test2.jpg",
            content=FileData.png,
            content_type="jpg",
        ),
        "image/jpeg",
        2,
    )

    to_category = category if same_category else category_factory()
    copied_doc = api.copy_document(input_doc, "CopyUser", "CopyGroup", to_category)
    files = copied_doc.files.order_by("variant", "created_at")

    assert copied_doc.title == "Bar (copy).pdf"
    assert copied_doc.category.pk == to_category.pk
    # document copy will have the user/group of the user who copied it
    assert copied_doc.created_by_user == "CopyUser"
    assert copied_doc.created_by_group == "CopyGroup"

    # 2 copied files + 2 new thumbnails
    assert len(files) == 4

    # original 1
    assert first_file.pk != files[0].pk
    assert files[0].document.pk == copied_doc.pk
    assert files[0].variant == File.Variant.ORIGINAL
    assert files[0].name == "Mee.pdf"
    assert files[0].mime_type == "image/png"
    assert files[0].size == 1
    # files will retain the user/group of the original document
    assert files[0].created_by_user == "Foo"
    assert files[0].created_by_group == "Baz"

    # new thumbnail for first file
    assert files[2].document.pk == copied_doc.pk
    assert files[2].variant == File.Variant.THUMBNAIL

    # original 2
    assert extra_file.pk != files[1].pk
    assert files[1].document.pk == copied_doc.pk
    assert files[1].variant == File.Variant.ORIGINAL
    assert files[1].name == "Mee2.pdf"
    assert files[1].mime_type == "image/jpeg"
    assert files[1].size == 2
    # files will retain the user/group of the original document
    assert files[1].created_by_user == "Foo2"
    assert files[1].created_by_group == "Baz2"

    # new thumbnail for extra file
    assert files[3].document.pk == copied_doc.pk
    assert files[3].variant == File.Variant.THUMBNAIL

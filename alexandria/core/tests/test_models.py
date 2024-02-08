import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from alexandria.core.factories import FileData
from alexandria.core.models import Document, File


@pytest.mark.parametrize("content_type", ["png", "unsupported"])
def test_clone_document(db, file_factory, content_type):
    original_file = file_factory(
        variant=File.Variant.ORIGINAL,
        content=SimpleUploadedFile(
            name="test.png",
            content=getattr(FileData, content_type),
            content_type=content_type,
        ),
    )

    if content_type != "unsupported":
        # generate original thumbnail
        file_factory(
            original=original_file,
            variant=File.Variant.THUMBNAIL,
            document=original_file.document,
        )

    original_document_pk = original_file.document.pk

    clone = original_file.document.clone()
    original = Document.objects.get(pk=original_document_pk)

    assert clone.pk != original.pk
    assert (
        clone.get_latest_original().content.name
        != original.get_latest_original().content.name
    )

    if content_type != "unsupported":
        assert clone.files.filter(variant=File.Variant.THUMBNAIL).exists()

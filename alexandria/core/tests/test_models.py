import pytest
from django.core.files import File as DjangoFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import ObjectDoesNotExist

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


def test_document_no_files(
    db,
    document_factory,
):
    document = document_factory.create()

    try:
        document.get_latest_original()
    except ObjectDoesNotExist:
        assert True


def test_clone_document_s3(db, mocker, settings, file_factory):
    settings.ALEXANDRIA_FILE_STORAGE = (
        "alexandria.storages.backends.s3.SsecGlobalS3Storage"
    )
    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = True
    name = "name-of-the-file"
    mocker.patch("storages.backends.s3.S3Storage.save", return_value=name)
    mocker.patch(
        "storages.backends.s3.S3Storage.open",
        return_value=DjangoFile(open("README.md", "rb")),
    )
    mocked = mocker.patch("botocore.client.BaseClient._make_api_call")

    original_file = file_factory(
        variant=File.Variant.ORIGINAL,
        content=SimpleUploadedFile(
            name="test.png",
            content=FileData.png,
            content_type="image/png",
        ),
    )

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
    assert mocked.call_args[0][1]["CopySource"]["Key"] == name

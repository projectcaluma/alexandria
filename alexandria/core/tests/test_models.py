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
    settings.ALEXANDRIA_FILE_STORAGE = "alexandria.storages.backends.s3.S3Storage"
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
        encryption_status=File.EncryptionStatus.SSEC_GLOBAL_KEY,
    )

    file_factory(
        original=original_file,
        variant=File.Variant.THUMBNAIL,
        document=original_file.document,
        encryption_status=File.EncryptionStatus.SSEC_GLOBAL_KEY,
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


@pytest.mark.parametrize(
    "input_file,output_name",
    [
        (
            # no document
            {"filename": "a_file.jpg", "title": None},
            "a_file.jpg",  # original name/title
        ),
        (
            # not renamed
            {"filename": "a_file.jpg", "title": "a_file.jpg"},
            "a_file.jpg",  # original name/title
        ),
        (
            # extension lost on rename
            {"filename": "b_file.jpg", "title": "b_file"},
            "b_file.jpg",  # extension recovered
        ),
        (
            # appended title after the extension
            {"filename": "b_file.jpg", "title": "b_file.jpg test"},
            "b_file.jpg test.jpg",  # extension recovered on appended title
        ),
        (
            # extension changed
            {"filename": "c_file.jpg", "title": "c_file.png"},
            "c_file.png.jpg",  # original extension recovered on top of renamed title
        ),
        (
            # double extension
            {"filename": "d_file.tar.gz", "title": "d_file.tar.gz"},
            "d_file.tar.gz",  # kept double extension
        ),
        (
            # unsafe filename, forbidden characters"
            {"filename": "test.txt", "title": 'test<>:"/\|?*.txt'},
            "test.txt",
        ),
        (
            # unsafe filename, windows drive letter ":"
            {"filename": "test.txt", "title": "c:\\test.txt"},
            "ctest.txt",
        ),
        (
            # unsafe filename, "space before extension"
            {"filename": "test.csv", "title": " test .csv"},
            "test.csv",
        ),
        # test for reserved keywords on Windows, e.g.:
        # CON, PRN, AUX, NUL,
        # COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9
        # LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9
        (
            # unsafe filename, "reserved keyword"
            {"filename": "test.txt", "title": "con.txt"},
            "con_.txt",
        ),
        (
            # unsafe filename, "reserved keyword"
            {"filename": "test.txt", "title": "LPT9.txt"},
            "LPT9_.txt",
        ),
        # e.g. COM10 is valid and should not be changed
        (
            {"filename": "test.txt", "title": "COM10.txt"},
            "COM10.txt",  # kept as is
        ),
    ],
)
def test_download_renamed(admin_client, file_factory, input_file, output_name):
    file = file_factory(
        name=input_file["filename"], document__title=input_file["title"] or ""
    )
    if not input_file["title"]:
        file.document = None

    base_name, extension = file.get_download_filename()
    assert base_name + extension == output_name

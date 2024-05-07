from io import StringIO

import pytest
import tika
from django.core.files import File as DjangoFile
from django.core.management import call_command

from alexandria.core.models import File
from alexandria.storages.backends.s3 import SsecGlobalS3Storage


def test_encrypt_files(db, settings, mocker, file_factory):
    file_old = file_factory(encryption_status=File.EncryptionStatus.NOT_ENCRYPTED)
    file_global = file_factory(encryption_status=File.EncryptionStatus.SSEC_GLOBAL_KEY)
    file_object = file_factory(encryption_status=File.EncryptionStatus.SSEC_OBJECT_KEY)

    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = True
    settings.ALEXANDRIA_ENCRYPTION_METHOD = File.EncryptionStatus.SSEC_GLOBAL_KEY.value
    settings.ALEXANDRIA_FILE_STORAGE = "alexandria.storages.backends.s3.S3Storage"

    mocker.patch("storages.backends.s3.S3Storage.save")
    mocker.patch("storages.backends.s3.S3Storage.open")
    SsecGlobalS3Storage.save.return_value = "name-of-the-file"
    SsecGlobalS3Storage.open.return_value = DjangoFile(open("README.md", "rb"))
    call_command("encrypt_files")

    file_old.refresh_from_db()
    file_global.refresh_from_db()
    file_object.refresh_from_db()

    assert SsecGlobalS3Storage.save.called_once()
    assert SsecGlobalS3Storage.open.called_once()
    assert file_old.encryption_status == File.EncryptionStatus.SSEC_GLOBAL_KEY
    assert file_global.encryption_status == File.EncryptionStatus.SSEC_GLOBAL_KEY
    assert file_object.encryption_status == File.EncryptionStatus.SSEC_OBJECT_KEY


@pytest.mark.parametrize(
    "enable_encryption,encryption_method",
    [
        (False, "ssec-global"),
        (True, File.EncryptionStatus.NOT_ENCRYPTED.value),
    ],
)
def test_encrypt_files_misconfigured(
    db, settings, file_factory, enable_encryption, encryption_method
):
    file_factory(encryption_status=File.EncryptionStatus.NOT_ENCRYPTED)

    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = enable_encryption
    settings.ALEXANDRIA_ENCRYPTION_METHOD = encryption_method

    out = StringIO()
    call_command("encrypt_files", stdout=out)

    assert "Encryption is not enabled. Skipping encryption of files." in out.getvalue()


def test_generate_content_vector(db, settings, file_factory):
    settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH = False
    file_without_vector = file_factory(name="old")

    settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH = True
    file_with_vector = file_factory(name="neu.docx")

    tika.parser.from_buffer.return_value = {"content": "Das ist Inhalt"}
    tika.language.from_buffer.return_value = "de"
    call_command("generate_content_vectors")

    file_with_vector.refresh_from_db()
    file_without_vector.refresh_from_db()

    assert tika.parser.from_buffer.called_once()
    assert tika.language.from_buffer.called_once()

    assert file_with_vector.content_vector == "'import':2B 'neu':1A 'text':3B"
    assert file_without_vector.content_vector == "'inhalt':4B 'old':1A"
    assert file_without_vector.language == "de"


def test_generate_content_vector_disabled(db, settings, file_factory):
    settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH = False

    out = StringIO()
    call_command("generate_content_vectors", stdout=out)

    assert (
        "Content search is not enabled. Skipping vectorization of file contents."
        in out.getvalue()
    )

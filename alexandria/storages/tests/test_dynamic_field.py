import pytest
from django.conf import ImproperlyConfigured

from alexandria.core.models import File
from alexandria.storages.backends.s3 import SsecGlobalS3Storage


@pytest.mark.parametrize("method", [File.EncryptionStatus.SSEC_GLOBAL_KEY.value])
@pytest.mark.parametrize(
    "secret,raises",
    [("".join(["x" for _ in range(32)]), None), ("too-short", ImproperlyConfigured)],
)
def test_dynamic_storage_select_global_ssec(
    db, settings, file_factory, method, secret, raises, mocker
):
    # set s3 compatible storage backend
    settings.ALEXANDRIA_FILE_STORAGE = "alexandria.storages.backends.s3.S3Storage"
    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = True

    settings.ALEXANDRIA_ENCRYPTION_METHOD = method
    settings.ALEXANDRIA_S3_STORAGE_SSEC_SECRET = secret

    mocker.patch("storages.backends.s3.S3Storage.save", return_value="name-of-the-file")
    # Patch away file opens
    mocker.patch("alexandria.core.tasks.set_checksum.delay", side_effect=None)
    mocker.patch("alexandria.core.tasks.set_content_vector.delay", side_effect=None)
    mocker.patch("alexandria.core.tasks.create_thumbnail.delay", side_effect=None)
    if raises is not None:
        with pytest.raises(raises):
            file_factory(encryption_status=settings.ALEXANDRIA_ENCRYPTION_METHOD)
        return
    file = file_factory(encryption_status=settings.ALEXANDRIA_ENCRYPTION_METHOD)
    SsecGlobalS3Storage.save.assert_called_once()

    # test copy file parameters through S3 copy
    mock_api_call = mocker.patch(
        "botocore.client.BaseClient._make_api_call", return_value=None
    )
    current_filename = file.content.name
    new_filename = "new-file-name"
    file.content.copy(new_filename)

    mock_api_call.assert_called_once()
    assert mock_api_call.call_args[0] == (
        "CopyObject",
        {
            "CopySource": {
                "Bucket": settings.ALEXANDRIA_S3_BUCKET_NAME,
                "Key": current_filename,
            },
            "CopySourceSSECustomerAlgorithm": "AES256",
            "CopySourceSSECustomerKey": settings.ALEXANDRIA_S3_STORAGE_SSEC_SECRET,
            "Bucket": settings.ALEXANDRIA_S3_BUCKET_NAME,
            "Key": new_filename,
            "SSECustomerAlgorithm": "AES256",
            "SSECustomerKey": settings.ALEXANDRIA_S3_STORAGE_SSEC_SECRET,
        },
    )


@pytest.mark.parametrize(
    "method,storage_backend",
    [
        (
            "invalid-encryption-mode",
            "alexandria.storages.backends.s3.S3Storage",
        ),
        (
            File.EncryptionStatus.NOT_ENCRYPTED.value,
            "alexandria.storages.backends.s3.S3Storage",
        ),
        (
            File.EncryptionStatus.SSEC_GLOBAL_KEY.value,
            "django.core.files.storage.FileSystemStorage",
        ),
    ],
)
def test_backend_configurations(db, settings, file_factory, method, storage_backend):
    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = True
    settings.ALEXANDRIA_FILE_STORAGE = storage_backend
    settings.ALEXANDRIA_ENCRYPTION_METHOD = method
    with pytest.raises(ImproperlyConfigured):
        file_factory()

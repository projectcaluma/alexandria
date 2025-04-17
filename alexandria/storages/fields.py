from pathlib import Path
from tempfile import NamedTemporaryFile

from django.conf import ImproperlyConfigured, settings
from django.core.files import File as DjangoFile
from django.core.files.storage import storages
from django.db import models
from django.db.models.fields.files import FieldFile
from storages.backends.s3 import S3Storage

from alexandria.storages.backends.s3 import SsecGlobalS3Storage


class DynamicStorageFieldFile(FieldFile):
    def __init__(self, instance, field, name):
        super().__init__(instance, field, name)
        storage_backend = settings.ALEXANDRIA_FILE_STORAGE
        if settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION:
            from alexandria.core.models import File

            if instance.encryption_status == File.EncryptionStatus.SSEC_GLOBAL_KEY:
                storage_backend = "alexandria.storages.backends.s3.SsecGlobalS3Storage"
        self.storage = storages.create_storage({"BACKEND": storage_backend})

    def copy(self, target_name: str):
        """
        Copy file content to target.

        NOTE: this will copy the content and this copy will be the new reference of the FileField.
        This means that there will be no pointer to the original content,
        unless you made a copy of the parent model instance beforhands by e.g.
        setting `file_instance.pk` to `None` before calling `file_instance.content.copy`.
        """
        # S3 compatible storage: copy in same bucket with s3 copy
        if isinstance(self.storage, S3Storage):
            copy_args = {
                "CopySource": {
                    "Bucket": self.storage.bucket.name,
                    "Key": self.name,
                },
                # Destination settings
                "Bucket": self.storage.bucket.name,
                "Key": target_name,
            }
            if isinstance(self.storage, SsecGlobalS3Storage):
                copy_args["CopySourceSSECustomerKey"] = self.storage.ssec_secret
                copy_args["CopySourceSSECustomerAlgorithm"] = "AES256"
                copy_args["SSECustomerKey"] = self.storage.ssec_secret
                copy_args["SSECustomerAlgorithm"] = "AES256"

            self.storage.bucket.meta.client.copy_object(**copy_args)
            self.instance.content = target_name
            self.instance.save()
            return

        # otherwise use filesystem storage
        with NamedTemporaryFile() as tmp:
            temp_file = Path(tmp.name)
            with temp_file.open("w+b") as file:
                file.write(self.read())
                self.instance.content = DjangoFile(file, target_name)
                self.instance.save()


class DynamicStorageFileField(models.FileField):
    attr_class = DynamicStorageFieldFile

    # TODO: When next working on file / storage stuff, consider extracting
    # the storage code into it's own project, so we can reuse it outside
    # of Alexandria: https://github.com/projectcaluma/alexandria/issues/480

    def __init__(self, storage=None, **kwargs):
        storage = storages.create_storage({"BACKEND": settings.ALEXANDRIA_FILE_STORAGE})
        super().__init__(storage=storage, **kwargs)

    def pre_save(self, instance, add):
        # set storage to default storage class to prevent reusing the last selection
        self.storage = storages.create_storage(
            {"BACKEND": settings.ALEXANDRIA_FILE_STORAGE}
        )
        if settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION:
            from alexandria.core.models import File

            method = settings.ALEXANDRIA_ENCRYPTION_METHOD
            if method not in File.EncryptionStatus.values:
                msg = (
                    f"ALEXANDRIA_ENCRYPTION_METHOD must be one of "
                    f"{File.EncryptionStatus.values}. {method} is not valid"
                )
                raise ImproperlyConfigured(msg)
            elif method == File.EncryptionStatus.NOT_ENCRYPTED.value:
                raise ImproperlyConfigured(
                    "ALEXANDRIA_ENCRYPTION_METHOD is set to NOT_ENCRYPTED while ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION is enabled."
                )
            if not isinstance(self.storage, S3Storage):
                msg = (
                    "At-rest object encryption is currently only available for S3 compatible storage backends. "
                    "Set `ALEXANDRIA_FILE_STORAGE` to `alexandria.storages.s3.S3Storage`."
                )
                raise ImproperlyConfigured(msg)
            if instance.encryption_status == File.EncryptionStatus.SSEC_GLOBAL_KEY:
                self.storage = storages.create_storage(
                    {"BACKEND": "alexandria.storages.backends.s3.SsecGlobalS3Storage"}
                )
        return super().pre_save(instance, add)

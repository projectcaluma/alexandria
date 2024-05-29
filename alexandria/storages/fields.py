from django.conf import ImproperlyConfigured, settings
from django.core.files.storage import storages
from django.db import models
from django.db.models.fields.files import FieldFile
from storages.backends.s3 import S3Storage

from alexandria.storages.backends.s3 import SsecGlobalS3Storage


class DynamicStorageFieldFile(FieldFile):
    def __init__(self, instance, field, name):
        super().__init__(instance, field, name)
        self.storage = storages.create_storage(
            {"BACKEND": settings.ALEXANDRIA_FILE_STORAGE}
        )
        if settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION:
            from alexandria.core.models import File

            if instance.encryption_status == File.EncryptionStatus.SSEC_GLOBAL_KEY:
                self.storage = SsecGlobalS3Storage()


class DynamicStorageFileField(models.FileField):
    attr_class = DynamicStorageFieldFile

    # TODO: When next working on file / storage stuff, consider extracting
    # the storage code into it's own project, so we can reuse it outside
    # of Alexandria: https://github.com/projectcaluma/alexandria/issues/480

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
            storage = SsecGlobalS3Storage()
            if instance.encryption_status == File.EncryptionStatus.SSEC_GLOBAL_KEY:
                self.storage = storage
        _file = super().pre_save(instance, add)
        return _file

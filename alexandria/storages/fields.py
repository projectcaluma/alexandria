from django.conf import ImproperlyConfigured, settings
from django.core.files.storage import get_storage_class
from django.db import models
from django.db.models.fields.files import FieldFile
from storages.backends.s3 import S3Storage

from alexandria.storages.backends.s3 import SsecGlobalS3Storage


class DynamicStorageFieldFile(FieldFile):
    def __init__(self, instance, field, name):
        super().__init__(instance, field, name)
        if (
            settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION
            and instance.encryption_status == instance.EncryptionStatus.SSEC_GLOBAL_KEY
        ):
            self.storage = SsecGlobalS3Storage()


class DynamicStorageFileField(models.FileField):
    attr_class = DynamicStorageFieldFile

    def pre_save(self, instance, add):
        # set storage to default storage class to prevent reusing the last selection
        DefaultStorage = get_storage_class()
        self.storage = DefaultStorage()
        if settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION:
            if (
                method := settings.ALEXANDRIA_ENCRYPTION_METHOD
            ) not in instance.EncryptionStatus.values:
                msg = (
                    f"ALEXANDRIA_ENCRYPTION_METHOD must be one of "
                    f"{instance.EncryptionStatus.values}. {method} is not valid"
                )
                raise ImproperlyConfigured(msg)
            if not isinstance(self.storage, S3Storage):
                msg = (
                    "At-rest object encryption is currently only available for S3 compatible storage backends. "
                    "Set `DEFAULT_FILE_STORAGE` to `alexandria.storages.s3.S3Storage`."
                )
                raise ImproperlyConfigured(msg)
            storage = SsecGlobalS3Storage()
            if instance.encryption_status == instance.EncryptionStatus.SSEC_GLOBAL_KEY:
                self.storage = storage
        _file = super().pre_save(instance, add)
        return _file

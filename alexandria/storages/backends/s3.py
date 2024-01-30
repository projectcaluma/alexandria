from django.conf import ImproperlyConfigured, settings as django_settings
from storages.backends.s3 import S3Storage as OriginalS3Storage
from storages.utils import setting


class S3Storage(OriginalS3Storage):
    def get_default_settings(self):
        return {
            **super().get_default_settings(),
            # required settings
            "access_key": setting("ALEXANDRIA_S3_ACCESS_KEY"),
            "secret_key": setting("ALEXANDRIA_S3_SECRET_KEY"),
            "endpoint_url": setting("ALEXANDRIA_S3_ENDPOINT_URL"),
            "bucket_name": setting("ALEXANDRIA_S3_BUCKET_NAME"),
            # optional settings
            "use_ssl": setting("ALEXANDRIA_S3_USE_SSL"),
            "verify": setting("ALEXANDRIA_S3_VERIFY"),
            "object_parameters": setting("ALEXANDRIA_S3_OBJECT_PARAMETERS", {}),
        }


class SsecGlobalS3Storage(S3Storage):
    def __init__(self, **settings):
        super().__init__(**settings)
        self.ssec_secret = django_settings.ALEXANDRIA_S3_STORAGE_SSEC_SECRET
        if len(key := self.ssec_secret) != 32:
            msg = f"ALEXANDRIA_S3_STORAGE_SSEC_SECRET keylength is: {len(key)}, expected length is 32"
            raise ImproperlyConfigured(msg)

    def get_object_parameters(self, name):  # pragma: no cover, TODO: cover
        params = super().get_object_parameters(name) or {}
        params.update(
            {"SSECustomerKey": self.ssec_secret, "SSECustomerAlgorithm": "AES256"}
        )
        return params

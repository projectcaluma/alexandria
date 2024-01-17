from django.conf import ImproperlyConfigured, settings as django_settings
from storages.backends.s3 import S3Storage


class SsecGlobalS3Storage(S3Storage):
    def __init__(self, **settings):
        super().__init__(**settings)
        self.ssec_secret = django_settings.AWS_S3_STORAGE_SSEC_SECRET
        if len(key := self.ssec_secret) != 32:
            msg = f"AWS_S3_STORAGE_SSEC_SECRET keylength is: {len(key)}, expected length is 32"
            raise ImproperlyConfigured(msg)

    def get_object_parameters(self, name):  # pragma: no cover, TODO: cover
        params = super().get_object_parameters(name) or {}
        params.update(
            {"SSECustomerKey": self.ssec_secret, "SSECustomerAlgorithm": "AES256"}
        )
        return params

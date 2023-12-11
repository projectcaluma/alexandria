from datetime import timedelta
from functools import wraps
from logging import getLogger

import minio
from django.conf import settings
from minio.commonconfig import CopySource

log = getLogger(__name__)


def _retry_on_missing_bucket(fn):
    """Create missing bucket if needed (decorator).

    If enabled in the settings, try to create the bucket if it
    doesn't exist yet, then retry.
    """

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except minio.error.S3Error as exc:  # pragma: todo cover
            if (
                exc.code == "NoSuchBucket"
                and settings.ALEXANDRIA_MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET
            ):
                log.warning(
                    f"Minio bucket '{self.bucket}' missing, trying to create it"
                )
                self.client.make_bucket(self.bucket)
                return fn(self, *args, **kwargs)
            raise

    return wrapper


class Minio:
    def __init__(self):
        endpoint = settings.ALEXANDRIA_MINIO_STORAGE_ENDPOINT
        access_key = settings.ALEXANDRIA_MINIO_STORAGE_ACCESS_KEY
        secret_key = settings.ALEXANDRIA_MINIO_STORAGE_SECRET_KEY
        secure = settings.ALEXANDRIA_MINIO_STORAGE_USE_HTTPS
        self.client = minio.Minio(
            endpoint, access_key=access_key, secret_key=secret_key, secure=secure
        )
        self.bucket = settings.ALEXANDRIA_MINIO_STORAGE_MEDIA_BUCKET_NAME

    @_retry_on_missing_bucket
    def download_url(self, object_name):
        return self.client.presigned_get_object(
            self.bucket,
            object_name,
            timedelta(minutes=settings.ALEXANDRIA_MINIO_PRESIGNED_TTL_MINUTES),
        )

    @_retry_on_missing_bucket
    def upload_url(self, object_name):
        return self.client.presigned_put_object(
            self.bucket,
            object_name,
            timedelta(minutes=settings.ALEXANDRIA_MINIO_PRESIGNED_TTL_MINUTES),
        )

    @_retry_on_missing_bucket
    def remove_object(self, object_name):
        self.client.remove_object(self.bucket, object_name)

    @_retry_on_missing_bucket
    def get_object(self, object_name):
        data = self.client.get_object(self.bucket, object_name)
        return data

    def copy_object(self, source_name, target_name):
        self.client.copy_object(
            self.bucket, target_name, CopySource(self.bucket, source_name)
        )


if settings.ALEXANDRIA_MEDIA_STORAGE_SERVICE == "minio":
    client = Minio()
else:  # pragma: no cover
    client = None
    raise NotImplementedError(
        f"Storage service {settings.ALEXANDRIA_MEDIA_STORAGE_SERVICE} is not implemented!"
    )

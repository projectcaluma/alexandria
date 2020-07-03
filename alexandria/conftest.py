import importlib
import inspect
import time

import pytest
from django.conf import settings
from django.core.cache import cache
from factory.base import FactoryMetaClass
from minio import Minio
from minio.definitions import Object as MinioStatObject
from pytest_factoryboy import register
from rest_framework.test import APIClient

from alexandria.oidc_auth.models import OIDCUser


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            # name needs to be compatible with
            # `rest_framework.routers.SimpleRouter` naming for easier testing
            base_name = obj._meta.model._meta.object_name.lower()
            register(obj, base_name)


register_module(importlib.import_module(".core.factories", "alexandria"))


@pytest.fixture
def admin_groups():
    return ["admin"]


@pytest.fixture
def admin_user(settings, admin_groups):
    return OIDCUser(
        "sometoken", {"sub": "admin", settings.OIDC_GROUPS_CLAIM: admin_groups}
    )


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture(scope="function", autouse=True)
def _autoclear_cache():
    cache.clear()


@pytest.fixture
def minio_mock(mocker):
    def side_effect(bucket, object_name, expires):
        return f"http://minio/download-url/{object_name}"

    stat_response = MinioStatObject(
        settings.MINIO_STORAGE_MEDIA_BUCKET_NAME,
        "some-file.pdf",
        time.struct_time((2019, 4, 5, 7, 0, 49, 4, 95, 0)),
        "0c81da684e6aaef48e8f3113e5b8769b",
        8200,
        content_type="application/pdf",
        is_dir=False,
        metadata={"X-Amz-Meta-Testtag": "super_file"},
    )
    mocker.patch.object(Minio, "presigned_get_object")
    mocker.patch.object(Minio, "presigned_put_object")
    mocker.patch.object(Minio, "stat_object")
    mocker.patch.object(Minio, "bucket_exists")
    mocker.patch.object(Minio, "make_bucket")
    mocker.patch.object(Minio, "remove_object")
    mocker.patch.object(Minio, "copy_object")
    Minio.presigned_get_object.side_effect = side_effect
    Minio.presigned_put_object.return_value = "http://minio/upload-url"
    Minio.stat_object.return_value = stat_response
    Minio.bucket_exists.return_value = True
    return Minio

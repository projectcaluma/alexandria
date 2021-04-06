import importlib
import inspect
import time
from io import BytesIO

import pytest
from django.core.cache import cache
from factory.base import FactoryMetaClass
from minio import Minio
from minio.definitions import Object as MinioStatObject
from pytest_factoryboy import register
from rest_framework.test import APIClient
from urllib3 import HTTPResponse

from alexandria.core.models import VisibilityMixin
from alexandria.core.serializers import BaseSerializer
from alexandria.core.tests import file_data
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
def user(settings, admin_groups):
    return OIDCUser("sometoken", {"sub": "user", settings.OIDC_GROUPS_CLAIM: ["group"]})


@pytest.fixture
def admin_user(settings, admin_groups):
    return OIDCUser(
        "sometoken", {"sub": "admin", settings.OIDC_GROUPS_CLAIM: admin_groups}
    )


@pytest.fixture
def client(db):
    client = APIClient()
    return client


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture(scope="function", autouse=True)
def _autoclear_cache():
    cache.clear()


@pytest.fixture
def reset_visibilities():
    before = VisibilityMixin.visibility_classes
    yield
    VisibilityMixin.visibility_classes = before


@pytest.fixture
def reset_validators():
    before = BaseSerializer.validation_classes
    yield
    BaseSerializer.validation_classes = before


@pytest.fixture
def preview_cache_dir(tmp_path, settings):
    settings.THUMBNAIL_CACHE_DIR = tmp_path
    return tmp_path


@pytest.fixture
def minio_mock(mocker, settings):
    def presigned_get_object_side_effect(bucket, object_name, expires):
        return f"http://minio/download-url/{object_name}"

    def get_object_side_effect(bucket, object_name):
        file = (
            file_data.unsupported
            if object_name.endswith(".unsupported")
            else file_data.png
        )
        return HTTPResponse(body=BytesIO(file), preload_content=False,)

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
    mocker.patch.object(Minio, "get_object")
    mocker.patch.object(Minio, "put_object")
    Minio.get_object.side_effect = get_object_side_effect
    Minio.presigned_get_object.side_effect = presigned_get_object_side_effect
    Minio.put_object.return_value = "af1421c17294eed533ec99eb82b468fb"
    Minio.presigned_put_object.return_value = "http://minio/upload-url"
    Minio.stat_object.return_value = stat_response
    Minio.bucket_exists.return_value = True
    return Minio

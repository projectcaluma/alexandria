import importlib
import inspect
import sys
import time
from io import BytesIO

import pytest
from django.core.cache import cache
from factory.base import FactoryMetaClass
from minio import Minio
from minio.datatypes import Object as MinioStatObject
from minio.helpers import ObjectWriteResult
from pytest_factoryboy import register
from pytest_factoryboy.fixture import Box
from rest_framework.test import APIClient
from urllib3 import HTTPResponse

from alexandria.core.models import VisibilityMixin
from alexandria.core.serializers import BaseSerializer
from alexandria.core.storage_clients import Minio as MinioStorageClient
from alexandria.core.tests import file_data
from alexandria.oidc_auth.models import OIDCUser


def register_module(module):
    # We need to pass the locals of this file to the register method to make
    # sure they are injected on the conftest locals instead of the default
    # locals which would be the locals of this function
    conftest_locals = Box(sys._getframe(1).f_locals)

    for _, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            register(obj, _caller_locals=conftest_locals)


register_module(importlib.import_module(".core.factories", "alexandria"))


@pytest.fixture
def admin_groups():
    return ["admin"]


@pytest.fixture
def user(settings, admin_groups):
    return OIDCUser(
        "sometoken",
        {settings.OIDC_USERNAME_CLAIM: "user", settings.OIDC_GROUPS_CLAIM: ["group"]},
    )


@pytest.fixture
def admin_user(settings, admin_groups):
    return OIDCUser(
        "sometoken",
        {
            settings.OIDC_USERNAME_CLAIM: "admin",
            settings.OIDC_GROUPS_CLAIM: admin_groups,
        },
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
def minio_mock(mocker, settings):
    def presigned_get_object_side_effect(bucket, object_name, expires):
        return f"http://minio/download-url/{object_name}"

    def get_object_side_effect(bucket, object_name):
        file = (
            file_data.unsupported
            if object_name.endswith(".unsupported")
            else file_data.png
        )
        return HTTPResponse(
            body=BytesIO(file),
            preload_content=False,
        )

    stat_response = MinioStatObject(
        settings.ALEXANDRIA_MINIO_STORAGE_MEDIA_BUCKET_NAME,
        "some-file.pdf",
        time.struct_time((2019, 4, 5, 7, 0, 49, 4, 95, 0)),
        "0c81da684e6aaef48e8f3113e5b8769b",
        8200,
        content_type="application/pdf",
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
    Minio.put_object.return_value = ObjectWriteResult(
        bucket_name=settings.ALEXANDRIA_MINIO_STORAGE_MEDIA_BUCKET_NAME,
        object_name="some-file.pdf",
        version_id="",
        etag="af1421c17294eed533ec99eb82b468fb",
        http_headers="",
    )
    Minio.presigned_put_object.return_value = "http://minio/upload-url"
    Minio.stat_object.return_value = stat_response
    Minio.bucket_exists.return_value = True
    return Minio


@pytest.fixture
def mock_s3storage(minio_mock, requests_mock):
    minio = MinioStorageClient()
    mock = requests_mock.put(minio.upload_url("the-object"), status_code=201)
    return mock

from pathlib import Path
from uuid import uuid4
from xml.dom import minidom

import boto3
import pytest
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.urls import reverse
from manabi.token import Key, Token
from moto import mock_aws
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from webtest import TestApp, TestRequest
from wsgidav.dav_error import HTTP_FORBIDDEN

from alexandria.core.models import File
from alexandria.dav import get_dav
from alexandria.dav_provider import AlexandriaProvider


@pytest.fixture
def s3(settings):
    with mock_aws():
        return boto3.client(
            "s3",
            endpoint_url=settings.ALEXANDRIA_S3_ENDPOINT_URL,
            aws_access_key_id=settings.ALEXANDRIA_S3_ACCESS_KEY,
            aws_secret_access_key=settings.ALEXANDRIA_S3_SECRET_KEY,
        )


@pytest.mark.parametrize("use_s3", [True, False])
@pytest.mark.parametrize("same_user", [True, False])
def test_dav(db, manabi, settings, s3, file_factory, use_s3, same_user):
    if use_s3:
        settings.ALEXANDRIA_FILE_STORAGE = "alexandria.storages.backends.s3.S3Storage"
    user = "admin"
    group = "admin"
    if same_user:
        user = "foobar"
        group = "foobar"
    with mock_aws():
        s3.create_bucket(Bucket=settings.ALEXANDRIA_S3_BUCKET_NAME)

        content_file = ContentFile(b"hello world", name="test.txt")
        file = file_factory(
            name="test.txt", content=content_file, size=content_file.size
        )
        file.modified_by_user = user
        file.modified_by_group = group
        file.save()
        dav_app = TestApp(get_dav())
        resp = dav_app.get(file.get_webdav_url("foobar", "foobar"))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.body == b"hello world"

        resp = dav_app.put(file.get_webdav_url("foobar", "foobar"), b"foo bar")
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        file.refresh_from_db()
        new_file = file
        document_files_count = 2
        if not same_user:
            document_files_count = 4
            new_file = (
                File.objects.filter(
                    document=file.document, variant=File.Variant.ORIGINAL
                )
                .exclude(pk=file.pk)
                .first()
            )
            assert file.modified_by_user == file.modified_by_group == "admin"

        assert file.document.files.count() == document_files_count
        assert new_file.size == new_file.content.size == 7
        assert new_file.modified_by_user == "foobar"
        new_file.content.seek(0)
        assert new_file.content.read() == b"foo bar"


@pytest.mark.freeze_time("1970-01-01")
def test_dav_propfind(db, manabi, file_factory, snapshot):
    content_file = ContentFile(b"hello world", name="test.txt")
    file = file_factory(name="test.txt", content=content_file, size=content_file.size)
    dav_app = TestApp(get_dav())
    url = file.get_webdav_url("foobar", "foobar")
    req = TestRequest.blank(url, method="PROPFIND", headers={"Depth": "1"})
    resp = dav_app.do_request(req)
    assert minidom.parseString(resp.body).toprettyxml(indent="  ") == snapshot


def test_dav_not_found(db, settings):
    key = Key.from_dictionary({"manabi": {"key": settings.MANABI_SHARED_KEY}})
    payload = ("username", "groupname", str(uuid4()))
    token = Token(key, Path("/"), payload=payload)

    assert (
        AlexandriaProvider("/").get_file_resource(
            "/",
            environ={"manabi.token": token, "wsgidav.provider": AlexandriaProvider},
            _=None,
        )
        is None
    )


def test_dav_file_infection(db, manabi, mocker, file_factory):
    mocker.patch(
        "alexandria.dav_provider.validate_file_infection",
        return_value=None,
        side_effect=ValidationError("File is infected with malware.", code="infected"),
    )

    content_file = ContentFile(b"hello world", name="test.txt")
    file = file_factory(name="test.txt", content=content_file, size=content_file.size)
    dav_app = TestApp(get_dav())
    url = file.get_webdav_url("foobar", "foobar")
    dav_app.put(url, b"foo bar", status=HTTP_FORBIDDEN)


@pytest.mark.parametrize("use_manabi", [True, False])
def test_dav_view(manabi, admin_client, document, file_factory, use_manabi, settings):
    settings.ALEXANDRIA_USE_MANABI = use_manabi
    content_file = ContentFile(b"hello world", name="test.txt")
    file = file_factory(name="test.txt", content=content_file, size=content_file.size)
    document.files.add(file)

    url = reverse("webdav-detail", args=[document.pk])
    response = admin_client.get(url)
    assert response.status_code == HTTP_200_OK
    dav_url = response.json()["data"]["attributes"]["webdav-url"]
    if use_manabi:
        assert dav_url.startswith("http://testserver/dav/")
        assert dav_url.endswith("test.txt")
    else:
        assert dav_url is None

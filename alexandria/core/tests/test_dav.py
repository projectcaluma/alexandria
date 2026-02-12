from datetime import timedelta
from pathlib import Path
from uuid import uuid4
from xml.dom import minidom

import boto3
import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.files.base import ContentFile
from django.urls import reverse
from manabi.token import Key, Token
from moto import mock_aws
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from webtest import TestApp, TestRequest
from webtest.app import AppError
from wsgidav.dav_error import HTTP_FORBIDDEN

from alexandria.core.models import File
from alexandria.dav import get_dav
from alexandria.dav_provider import AlexandriaProvider

TestRequest.__test__ = False


@pytest.fixture
def s3(settings):
    with mock_aws():
        return boto3.client(
            "s3",
            endpoint_url=settings.ALEXANDRIA_S3_ENDPOINT_URL,
            aws_access_key_id=settings.ALEXANDRIA_S3_ACCESS_KEY,
            aws_secret_access_key=settings.ALEXANDRIA_S3_SECRET_KEY,
        )


def get_webdav_url_without_uri_scheme(file, *args):
    uri = file.get_webdav_url(*args)

    return uri.split("|")[-1]


@pytest.mark.parametrize("use_s3", [True, False])
@pytest.mark.parametrize("same_user", [True, False])
def test_dav(db, manabi, settings, s3, file_factory, use_s3, same_user):
    settings.ALEXANDRIA_MANABI_DAV_URI_SCHEMES = {"text/plain": "ms-word:ofe|u|"}

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
            name="test.txt",
            content=content_file,
            size=content_file.size,
            mime_type="text/plain",
        )
        file.modified_by_user = user
        file.modified_by_group = group
        file.save()
        modified_before = file.document.modified_at
        dav_app = TestApp(get_dav())
        resp = dav_app.get(get_webdav_url_without_uri_scheme(file, "foobar", "foobar"))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.body == b"hello world"

        resp = dav_app.put(
            get_webdav_url_without_uri_scheme(file, "foobar", "foobar"), b"foo bar"
        )
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
        assert (new_file.document.modified_at - modified_before).microseconds > 0


@pytest.mark.freeze_time("1970-01-01")
def test_dav_propfind(db, manabi, file_factory, snapshot):
    settings.ALEXANDRIA_MANABI_DAV_URI_SCHEMES = {"text/plain": "ms-word:ofe|u|"}

    content_file = ContentFile(b"hello world", name="test.txt")
    file = file_factory(
        pk="5fa8513e-7d50-46de-addb-5abaa6e1478e",
        name="test.txt",
        content=content_file,
        size=content_file.size,
        mime_type="text/plain",
    )
    dav_app = TestApp(get_dav())
    url = get_webdav_url_without_uri_scheme(file, "foobar", "foobar")
    req = TestRequest.blank(url, method="PROPFIND", headers={"Depth": "1"})
    resp = dav_app.do_request(req)
    assert minidom.parseString(resp.body).toprettyxml(indent="  ") == snapshot


def test_dav_not_found(db, settings):
    key = Key.from_dictionary({"manabi": {"key": settings.MANABI_SHARED_KEY}})
    payload = ("username", "groupname")
    path = Path(str(uuid4())) / Path("myfile.docx")
    token = Token(key, path, payload=payload)

    assert (
        AlexandriaProvider("/").get_file_resource(
            f"/{str(path)}",
            environ={"manabi.token": token, "wsgidav.provider": AlexandriaProvider},
            _=None,
        )
        is None
    )


def test_dav_file_infection(db, manabi, mocker, file_factory):
    mocker.patch(
        "alexandria.core.validations.validate_file_infection",
        return_value=None,
        side_effect=ValidationError("File is infected with malware.", code="infected"),
    )

    content_file = ContentFile(b"hello world", name="test.txt")
    file = file_factory(name="test.txt", content=content_file, size=content_file.size)
    settings.ALEXANDRIA_MANABI_DAV_URI_SCHEMES = {file.mime_type: "ms-word:ofe|u|"}
    dav_app = TestApp(get_dav())
    url = get_webdav_url_without_uri_scheme(file, "foobar", "foobar")
    dav_app.put(url, b"foo bar", status=HTTP_FORBIDDEN)


@pytest.mark.parametrize(
    "use_manabi,mime_type,expected_status",
    [
        (
            True,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            HTTP_200_OK,
        ),
        (True, "image/png", HTTP_404_NOT_FOUND),
        (
            False,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            HTTP_404_NOT_FOUND,
        ),
    ],
)
def test_dav_view(
    manabi,
    settings,
    admin_client,
    document,
    file_factory,
    use_manabi,
    mime_type,
    expected_status,
):
    settings.ALEXANDRIA_USE_MANABI = use_manabi
    content_file = ContentFile(b"hello world", name="test.txt")
    file = file_factory(
        name="test.txt",
        content=content_file,
        size=content_file.size,
        mime_type=mime_type,
    )
    document.files.add(file)

    url = reverse("webdav-detail", args=[document.pk])
    response = admin_client.get(url)

    assert response.status_code == expected_status
    if expected_status == HTTP_200_OK:
        dav_url = response.json()["data"]["attributes"]["webdav-url"]
        assert dav_url.startswith("ms-word:ofe|u|http://testserver/dav/")
        assert dav_url.endswith("test.txt")


@pytest.mark.parametrize(
    "mime_type,expected_scheme", settings.ALEXANDRIA_MANABI_DAV_URI_SCHEMES.items()
)
def test_dav_url_schemes(
    admin_client,
    document,
    expected_scheme,
    file_factory,
    manabi,
    mime_type,
):
    document.files.add(file_factory(mime_type=mime_type))

    url = reverse("webdav-detail", args=[document.pk])
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    dav_url = response.json()["data"]["attributes"]["webdav-url"]
    assert dav_url.startswith(expected_scheme)


def test_dav_url_schemes_unconfigured(db, file_factory, manabi, settings):
    mime_type = "application/vnd.ms-word.document.macroenabled.12"  # .docm

    settings.ALEXANDRIA_MANABI_ALLOWED_MIMETYPES = [mime_type]
    settings.ALEXANDRIA_MANABI_DAV_URI_SCHEMES = {}

    file = file_factory(mime_type=mime_type)

    with pytest.raises(ImproperlyConfigured) as e:
        file.get_webdav_url("foobar", "foobar")

    assert str(e.value).startswith(f'The MIME type "{mime_type}"')


def test_dav_without_content(db, manabi, settings, file_factory):
    settings.ALEXANDRIA_MANABI_DAV_URI_SCHEMES = {"text/plain": "ms-word:ofe|u|"}

    file = file_factory(
        name="test.txt",
        mime_type="text/plain",
        modified_by_user="some-user",
        modified_by_group="some-group",
    )

    dav_app = TestApp(get_dav())

    with pytest.raises(AppError) as e:
        dav_app.put(
            get_webdav_url_without_uri_scheme(
                file,
                "some-other-user",
                "some-other-group",
            ),
            b"",
        )

    assert "400 Bad Request" in str(e)
    assert file.document.files.filter(variant=File.Variant.ORIGINAL).count() == 1


@pytest.mark.parametrize(
    ("user", "group", "seconds_since_last_modification", "should_create_version"),
    [
        ("some-user", "some-group", 0, False),
        ("other-user", "some-group", 0, True),
        ("some-user", "other-group", 0, True),
        ("some-user", "some-group", 29 * 60, False),
        ("some-user", "some-group", 45 * 60, True),
    ],
)
def test_dav_versioning(
    db,
    file_factory,
    freezer,
    group,
    manabi,
    seconds_since_last_modification,
    settings,
    should_create_version,
    user,
):
    settings.ALEXANDRIA_MANABI_DAV_URI_SCHEMES = {"text/plain": "ms-word:ofe|u|"}
    settings.ALEXANDRIA_MANABI_VERSION_CREATION_THRESHOLD_ENABLED = True
    settings.ALEXANDRIA_MANABI_VERSION_CREATION_THRESHOLD_SECONDS = 30 * 60

    file = file_factory(
        name="test.txt",
        mime_type="text/plain",
        modified_by_user="some-user",
        modified_by_group="some-group",
    )

    freezer.move_to(
        file.modified_at + timedelta(seconds=seconds_since_last_modification)
    )

    dav_app = TestApp(get_dav())

    response = dav_app.put(
        get_webdav_url_without_uri_scheme(file, user, group),
        b"foobar",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert (
        file.document.files.filter(variant=File.Variant.ORIGINAL)
        .exclude(pk=file.pk)
        .exists()
        == should_create_version
    )

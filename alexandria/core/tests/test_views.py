import io
import uuid
import zipfile

import pytest
from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone
from factory.django import django_files
from PIL import Image
from preview_generator.manager import PreviewManager
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from alexandria.core.factories import FileData
from alexandria.core.models import File
from alexandria.core.tests.test_permissions import TIMESTAMP

from ..models import Document, Tag
from ..views import DocumentViewSet, FileViewSet, TagViewSet


@pytest.mark.parametrize("allow_anon", [True, False])
@pytest.mark.parametrize("method", ["post", "patch"])
def test_anonymous_writing(db, document, client, settings, user, allow_anon, method):
    settings.ALEXANDRIA_ALLOW_ANONYMOUS_WRITE = allow_anon
    if not allow_anon:
        settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
            "rest_framework.permissions.IsAuthenticatedOrReadOnly",
        ]

    data = {"data": {"type": "documents", "attributes": {"title": "winstonsmith"}}}

    url = reverse("document-list")

    if method == "patch":
        data["data"]["id"] = str(document.pk)
        url = reverse("document-detail", args=[document.pk])

    resp = getattr(client, method)(url, data=data)
    assert (
        resp.status_code == HTTP_201_CREATED or HTTP_200_OK
        if allow_anon
        else HTTP_403_FORBIDDEN
    )


@pytest.mark.parametrize("enable_checksum", (True, False))
@pytest.mark.parametrize(
    "file_variant,enable_thumbnails,existing_thumbnail,file_type,original,status_code",
    [
        (File.Variant.ORIGINAL, True, False, "png", False, HTTP_201_CREATED),
        # Original cannot also relate to another original
        (File.Variant.ORIGINAL, True, False, "png", True, HTTP_400_BAD_REQUEST),
        (File.Variant.THUMBNAIL, True, False, "png", True, HTTP_201_CREATED),
        # thumbnail requires original
        (File.Variant.THUMBNAIL, True, True, "png", False, HTTP_400_BAD_REQUEST),
        (File.Variant.THUMBNAIL, True, True, "png800", True, HTTP_201_CREATED),
        # Variant is required
        (None, True, True, "png", False, HTTP_400_BAD_REQUEST),
        (File.Variant.ORIGINAL, True, True, "unsupported", False, HTTP_201_CREATED),
        (
            File.Variant.THUMBNAIL,
            True,
            False,
            "unsupported",
            True,
            HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_file_upload(
    admin_client,
    document_factory,
    tmp_path,
    file_factory,
    file_variant,
    existing_thumbnail,
    enable_thumbnails,
    enable_checksum,
    file_type,
    original,
    status_code,
    settings,
):
    settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION = enable_thumbnails
    settings.ALEXANDRIA_ENABLE_CHECKSUM = enable_checksum
    doc = document_factory()
    data = {
        "name": "file.png",
        "document": str(doc.pk),
        "content": io.BytesIO(getattr(FileData, file_type)),
    }
    if file_variant:
        data["variant"] = file_variant
    if original:
        file_ = file_factory(document=doc, variant=File.Variant.ORIGINAL)
        data["original"] = str(file_.pk)
        if existing_thumbnail:
            thumb = file_factory(
                document=doc, variant=File.Variant.THUMBNAIL, original=file_
            )
    url = reverse("file-list")
    resp = admin_client.post(url, data=data, format="multipart")

    assert resp.status_code == status_code
    doc.refresh_from_db()

    if status_code < HTTP_400_BAD_REQUEST:
        assert doc.files.filter(name="file.png", variant=file_variant).exists()
    # No document should have more than one original or thumbnail
    assert (
        not Document.objects.annotate(
            thumb_cnt=Count(
                "files", filter=Q(**{"files__variant": File.Variant.THUMBNAIL})
            )
        )
        .filter(thumb_cnt__gt=1)
        .exists()
    )
    # check that no thumbnails are larger than configured aka uploaded thumbnails are
    # in fact resized:
    for thumb in File.objects.filter(variant=File.Variant.THUMBNAIL).iterator():
        width, height = Image.open(thumb.content.file).size
        assert not any(
            [
                width > (settings.ALEXANDRIA_THUMBNAIL_WIDTH or 256),
                height > (settings.ALEXANDRIA_THUMBNAIL_HEIGHT or 256),
            ]
        )

    if enable_checksum and status_code < HTTP_400_BAD_REQUEST:
        if file_variant == File.Variant.THUMBNAIL:
            # the thumbnail checksum will not necessarily be calculated from the
            # uploaded file but from the rezised version.
            # To emulate this behaviour we first need to store the uploaded file
            # because PreviewManager does not accept in-memory byte streams
            uploaded = tmp_path / f"uploaded.{file_type}"
            with uploaded.open("wb") as f:
                f.write(getattr(FileData, file_type))
            manager = PreviewManager(tmp_path)
            preview_path = manager.get_jpeg_preview(str(uploaded))
            with open(preview_path, "rb") as f:
                checksum = File.make_checksum(f.read())
                assert (
                    doc.files.filter(variant=File.Variant.THUMBNAIL).first().checksum
                    == checksum
                )
        elif file_variant == File.Variant.ORIGINAL:
            assert doc.files.filter(
                variant=File.Variant.ORIGINAL
            ).first().checksum == File.make_checksum(getattr(FileData, file_type))
        else:
            pass


def test_at_rest_encryption(admin_client, settings, document, mocker):
    mocker.patch("storages.backends.s3.S3Storage.save", return_value="file-name")
    storage_file = mocker.MagicMock()
    storage_file.file = django_files.temp.tempfile.SpooledTemporaryFile("rb")
    mocker.patch(
        "storages.backends.s3.S3Storage.open",
        return_value=storage_file,
    )
    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = True
    settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION = False
    settings.ALEXANDRIA_ENCRYPTION_METHOD = File.EncryptionStatus.SSEC_GLOBAL_KEY
    settings.DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
    data = {
        "name": "file.png",
        "document": str(document.pk),
        "content": io.BytesIO(FileData.png),
        "variant": File.Variant.ORIGINAL,
    }
    response = admin_client.post(reverse("file-list"), data=data, format="multipart")
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.parametrize(
    "admin_groups, update, active_group, expect_response",
    [
        (["foo", "bar"], False, "foo", HTTP_201_CREATED),
        (["foo", "bar"], False, None, HTTP_201_CREATED),
        (["foo", "bar"], True, "foo", HTTP_200_OK),
        (["somegroup"], True, "foo", HTTP_200_OK),
        (["somegroup"], True, "somegroup", HTTP_200_OK),
        (["foobar"], True, "somegroup", HTTP_200_OK),
    ],
)
@pytest.mark.parametrize("viewset", [DocumentViewSet, FileViewSet, TagViewSet])
def test_validate_created_by_group(
    db,
    settings,
    viewset,
    request,
    update,
    admin_client,
    active_group,
    expect_response,
):
    viewset_inst = viewset()
    model_class = viewset_inst.queryset.model
    model_name = model_class.__name__.lower()
    model = request.getfixturevalue(f"{model_name}_factory").create(
        created_by_group="somegroup"
    )
    serializer = viewset_inst.serializer_class()
    serialized_model = serializer.to_representation(model)
    serialized_model["created_by_group"] = active_group
    del serialized_model["modified_by_group"]

    if not update:
        # delete model in the DB so we can then create it via API
        model.delete()

    post_data = {
        "data": {
            "attributes": serialized_model,
            "type": model_class._meta.verbose_name_plural,
        }
    }
    if update:
        post_data["data"]["id"] = str(model.pk)

    if model_name == "file" and update:
        # PATCH on files not implemented, but I don't wanna
        # not test it on POST
        return

    if viewset == FileViewSet and not update:
        del post_data["data"]
        for key in ["variant", "name", "original"]:
            post_data[key] = serialized_model[key]
        if post_data["original"] is None:
            del post_data["original"]

        post_data["content"] = io.BytesIO(b"datadatatatat")
        post_data["document"] = serialized_model["document"]["id"]

    if update:
        request_meth = admin_client.patch
        url = reverse(f"{model_name}-detail", args=[model.pk])
        # updates are not allowed to change created_by_group
        model.refresh_from_db()
        assert model.created_by_group == "somegroup"
    else:
        request_meth = admin_client.post
        url = reverse(f"{model_name}-list")

    response = (
        request_meth(url, post_data, format="multipart")
        if viewset == FileViewSet
        else request_meth(url, post_data)
    )
    assert response.status_code == expect_response


@pytest.mark.parametrize(
    "field,value",
    [
        ("created_at", "test"),
        ("created_by_user", "test"),
        ("created_by_group", "test"),
    ],
)
def test_created_validation(admin_client, document_factory, field, value):
    document = document_factory()

    url = reverse("document-detail", args=[document.pk])

    data = {
        "data": {
            "type": "documents",
            "id": document.pk,
            "attributes": {
                field: value,
            },
        }
    }

    response = admin_client.patch(url, data=data)

    result = response.json()
    assert result["data"]["attributes"][field.replace("_", "-")] != value
    assert result["data"]["attributes"][field.replace("_", "-")] is not None

    document.refresh_from_db()
    assert getattr(document, field) != value


def test_multi_download(admin_client, file_factory):
    file_factory(name="my_file3.png")  # should not be returned
    file1 = file_factory(name="a_file(1)")
    file2 = file_factory(name="a_file")
    file3 = file_factory(name="a_file")
    file4 = file_factory(name="b_file.png")

    url = reverse("file-multi")

    resp = admin_client.get(
        url,
        {
            "filter[files]": f"{str(file1.pk)},{str(file2.pk)},{str(file3.pk)},{str(file4.pk)}"
        },
    )
    assert resp.status_code == HTTP_200_OK
    assert resp.filename == "files.zip"

    zip_buffer = io.BytesIO()
    for c in resp.streaming_content:
        zip_buffer.write(c)
    zip = zipfile.ZipFile(zip_buffer)

    assert len(zip.filelist) == 4
    filelist = sorted(zip.filelist, key=lambda a: a.filename)
    assert filelist[0].filename == "a_file"
    assert zip.open("a_file").read() == file2.content.file.read()
    assert filelist[1].filename == "a_file(1)"
    assert zip.open("a_file(1)").read() == file1.content.file.read()
    assert filelist[2].filename == "a_file(2)"
    assert zip.open("a_file(2)").read() == file3.content.file.read()
    assert filelist[3].filename == "b_file.png"
    assert zip.open(file4.name).read() == file4.content.file.read()


@pytest.mark.parametrize(
    "params,expected_status",
    [
        ({}, HTTP_400_BAD_REQUEST),
        ({"filter[files]": str(uuid.uuid4())}, HTTP_404_NOT_FOUND),
        ({"filter[files]": "no uuid"}, HTTP_400_BAD_REQUEST),
    ],
)
def test_multi_download_failure(admin_client, params, expected_status):
    url = reverse("file-multi")

    resp = admin_client.get(url, params)
    assert resp.status_code == expected_status


def test_document_delete_some_tags(admin_client, tag_factory, document_factory):
    """Test clearing of unused tags."""
    tag_1, tag_2, tag_3, tag_4 = tag_factory.create_batch(4)

    # document from which we delete tags
    document_1 = document_factory()
    document_1.tags.add(tag_1, tag_2, tag_3, tag_4)
    document_1.save()

    # docuemnt with tags, that can't be deleted
    document_2 = document_factory()
    document_2.tags.add(tag_3)
    document_2.save()

    url = reverse("document-detail", args=[document_1.id])

    data = {
        "data": {
            "type": "documents",
            "id": document_1.id,
            "relationships": {
                "tags": {
                    "data": [
                        {"id": tag_1.pk, "type": "tags"},
                        {"id": tag_2.pk, "type": "tags"},
                    ]
                }
            },
        }
    }

    response = admin_client.patch(url, data)

    assert response.status_code == HTTP_200_OK
    assert Tag.objects.all().count() == 3
    assert set(Tag.objects.all().values_list("pk", flat=True)) == set(
        [tag_1.pk, tag_2.pk, tag_3.pk]
    )


@pytest.mark.parametrize(
    "presigned, expected_status",
    [(True, HTTP_200_OK), (False, HTTP_403_FORBIDDEN)],
)
def test_download_file(admin_client, file, presigned, expected_status):
    if not presigned:
        url = reverse("file-download", args=[file.pk])
    else:
        response = admin_client.get(reverse("file-detail", args=(file.pk,)))
        url = response.json()["data"]["attributes"]["download-url"]

    result = admin_client.get(url)
    assert result.status_code == expected_status


@pytest.mark.freeze_time(TIMESTAMP, as_arg=True)
def test_presigned_url_expired(admin_client, client, file, freezer, settings):
    response = admin_client.get(reverse("file-detail", args=(file.pk,)))
    url = response.json()["data"]["attributes"]["download-url"]
    freezer.tick(
        delta=timezone.timedelta(seconds=settings.ALEXANDRIA_DOWNLOAD_URL_LIFETIME + 5)
    )
    response = client.get(url)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_presigned_url_tempered_signature(admin_client, client, file):
    response = admin_client.get(reverse("file-detail", args=(file.pk,)))
    url = response.json()["data"]["attributes"]["download-url"]
    without_params, params = url.split("?")
    expiry, signature = params.split("&")
    key, val = expiry.split("=")
    val = str(int(val) + 1000)
    url = f"{without_params}?{signature}&{key}={val}"
    response = client.get(url)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_presigned_url_different_file(admin_client, file, file_factory):
    response = admin_client.get(reverse("file-detail", args=(file.pk,)))
    url = response.json()["data"]["attributes"]["download-url"]

    other_file = file_factory()
    url = url.replace(str(file.pk), str(other_file.pk))

    response = admin_client.get(url)
    assert response.status_code == HTTP_400_BAD_REQUEST

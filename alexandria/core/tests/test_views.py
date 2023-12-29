import io
import uuid
import zipfile

import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from alexandria.core.models import File

from ..models import Tag
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


@pytest.mark.parametrize(
    "file_variant,original,status_code",
    [
        (File.ORIGINAL, False, HTTP_201_CREATED),
        (File.THUMBNAIL, True, HTTP_201_CREATED),
        (File.THUMBNAIL, False, HTTP_400_BAD_REQUEST),
        (File.ORIGINAL, True, HTTP_400_BAD_REQUEST),
        (None, False, HTTP_400_BAD_REQUEST),
    ],
)
def test_file_validation(
    minio_mock,
    admin_client,
    document_factory,
    file_factory,
    file_variant,
    original,
    status_code,
):
    doc = document_factory()

    data = {
        "data": {
            "type": "files",
            "attributes": {"name": "file.pdf"},
            "relationships": {
                "document": {"data": {"id": str(doc.pk), "type": "documents"}},
            },
        }
    }
    if file_variant:
        data["data"]["attributes"]["variant"] = file_variant
    if original:
        file = file_factory(document=doc, name="file2.pdf")
        data["data"]["relationships"]["original"] = {
            "data": {"id": str(file.pk), "type": "files"},
        }

    url = reverse("file-list")

    resp = admin_client.post(url, data=data)
    assert resp.status_code == status_code


@pytest.mark.parametrize(
    "enabled,method,correct_bucket,supported_mime,is_thumb,status_code",
    [
        (True, "head", True, True, False, HTTP_200_OK),
        (True, "post", True, True, False, HTTP_201_CREATED),
        (True, "post", True, False, False, HTTP_200_OK),
        (True, "post", True, True, False, HTTP_400_BAD_REQUEST),
        (True, "post", False, True, False, HTTP_200_OK),
        (True, "post", True, True, True, HTTP_200_OK),
        (False, "post", True, True, False, HTTP_403_FORBIDDEN),
    ],
)
def test_hook_view(
    admin_client,
    minio_mock,
    mock_s3storage,
    document_factory,
    settings,
    enabled,
    method,
    correct_bucket,
    supported_mime,
    is_thumb,
    status_code,
):
    url = reverse("hook")
    data = {
        "EventName": "s3:ObjectCreated:Put",
        "Key": "alexandria-media/218b2504-1736-476e-9975-dc5215ef4f01_test.png",
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "minio:s3",
                "awsRegion": "",
                "eventTime": "2020-07-17T06:38:23.221Z",
                "eventName": "s3:ObjectCreated:Put",
                "userIdentity": {"principalId": "minio"},
                "requestParameters": {
                    "accessKey": "minio",
                    "region": "",
                    "sourceIPAddress": "172.20.0.1",
                },
                "responseElements": {
                    "x-amz-request-id": "162276DB8350E531",
                    "x-minio-deployment-id": "5db7c8da-79cb-4d3a-8d40-189b51ca7aa6",
                    "x-minio-origin-endpoint": "http://172.20.0.2:9000",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "Config",
                    "bucket": {
                        "name": "alexandria-media",
                        "ownerIdentity": {"principalId": "minio"},
                        "arn": "arn:aws:s3:::alexandria-media",
                    },
                    "object": {
                        "key": "218b2504-1736-476e-9975-dc5215ef4f01_test.png",
                        "size": 299758,
                        "eTag": "af1421c17294eed533ec99eb82b468fb",
                        "contentType": "application/pdf",
                        "userMetadata": {"content-variant": "application/pdf"},
                        "versionId": "1",
                        "sequencer": "162276DB83A9F895",
                    },
                },
                "source": {
                    "host": "172.20.0.1",
                    "port": "",
                    "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.0 Chrome/80.0.3987.163 Safari/537.36",
                },
            }
        ],
    }

    settings.ALEXANDRIA_ENABLE_CHECKSUM = False
    settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION = enabled

    if status_code == HTTP_201_CREATED:
        doc = document_factory()
        File.objects.create(
            document=doc, name="test.png", pk="218b2504-1736-476e-9975-dc5215ef4f01"
        )
        assert File.objects.count() == 1

    if not supported_mime:
        doc = document_factory()
        File.objects.create(
            document=doc,
            name="test.unsupported",
            pk="218b2504-1736-476e-9975-dc5215ef4f01",
        )
        assert File.objects.count() == 1
        data["Records"][0]["s3"]["object"][
            "name"
        ] = "218b2504-1736-476e-9975-dc5215ef4f01_test.unsupported"

    if is_thumb:
        doc = document_factory()
        File.objects.create(
            document=doc,
            name="test.png",
            pk="218b2504-1736-476e-9975-dc5215ef4f01",
            variant=File.THUMBNAIL,
        )
        assert File.objects.count() == 1

    if not correct_bucket:
        data["Records"][0]["s3"]["bucket"]["name"] = "wrong-bucket"

    resp = getattr(admin_client, method)(url, data=data if method == "post" else None)
    assert resp.status_code == status_code

    if status_code == HTTP_201_CREATED:
        assert File.objects.count() == 2
        assert File.objects.filter(variant=File.THUMBNAIL).count() == 1
        orig = File.objects.get(variant=File.ORIGINAL)
        thumb = File.objects.get(variant=File.THUMBNAIL)
        assert thumb.original == orig
        assert orig.upload_status == File.COMPLETED
        assert thumb.upload_status == File.COMPLETED

    if is_thumb:
        assert File.objects.count() == 1


@pytest.mark.parametrize(
    "variant,enabled,existing_thumbnail,file_name,status_code",
    [
        (File.ORIGINAL, True, False, "foo.jpg", HTTP_201_CREATED),
        (File.ORIGINAL, True, False, "foo.unsupported", HTTP_400_BAD_REQUEST),
        (File.ORIGINAL, False, False, "foo.jpg", HTTP_400_BAD_REQUEST),
        (File.ORIGINAL, True, True, "foo.jpg", HTTP_400_BAD_REQUEST),
        (File.THUMBNAIL, True, False, "foo.jpg", HTTP_400_BAD_REQUEST),
    ],
)
def test_manual_thumbnail(
    minio_mock,
    mock_s3storage,
    settings,
    admin_client,
    file_factory,
    variant,
    enabled,
    existing_thumbnail,
    file_name,
    status_code,
):
    settings.ALEXANDRIA_ENABLE_CHECKSUM = False
    settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION = enabled

    file = file_factory(variant=variant, name=file_name)

    if existing_thumbnail:
        file_factory(variant=File.THUMBNAIL, original=file)

    data = {
        "data": {
            "type": "files",
            "id": file.pk,
        }
    }
    url = reverse("file-generate-thumbnail", args=[file.pk])

    resp = admin_client.post(url, data)
    assert resp.status_code == status_code

    if status_code == HTTP_201_CREATED:
        file.refresh_from_db()
        assert File.objects.count() == 2
        assert File.objects.filter(variant=File.THUMBNAIL).count() == 1
        thumb = File.objects.get(variant=File.THUMBNAIL)
        assert thumb.original == file
        assert file.upload_status == File.COMPLETED
        assert thumb.upload_status == File.COMPLETED
    else:
        assert File.objects.count() == 1 + int(existing_thumbnail)


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
    minio_mock,
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

    if update:
        request_meth = admin_client.patch
        url = reverse(f"{model_name}-detail", args=[model.pk])
        # updates are not allowed to change created_by_group
        model.refresh_from_db()
        assert model.created_by_group == "somegroup"
    else:
        request_meth = admin_client.post
        url = reverse(f"{model_name}-list")

    response = request_meth(url, post_data)
    assert response.status_code == expect_response


def test_multi_download(admin_client, minio_mock, file_factory):
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
    assert zip.open("a_file").read() == b"a_file"
    assert filelist[1].filename == "a_file(1)"
    assert zip.open("a_file(1)").read() == b"a_file(1)"
    assert filelist[2].filename == "a_file(2)"
    assert zip.open("a_file(2)").read() == b"a_file"
    assert filelist[3].filename == "b_file.png"
    assert zip.open(file4.name).read() == b"b_file.png"


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
                        {"id": tag_1.slug, "type": "tags"},
                        {"id": tag_2.slug, "type": "tags"},
                    ]
                }
            },
        }
    }

    response = admin_client.patch(url, data)

    assert response.status_code == HTTP_200_OK
    assert Tag.objects.all().count() == 3
    assert set(Tag.objects.all().values_list("slug", flat=True)) == set(
        [tag_1.slug, tag_2.slug, tag_3.slug]
    )


@pytest.mark.parametrize(
    "enabled,status_code", [(True, HTTP_201_CREATED), (False, HTTP_403_FORBIDDEN)]
)
def test_checksum(
    admin_client,
    minio_mock,
    mock_s3storage,
    document_factory,
    settings,
    enabled,
    status_code,
):
    data = {
        "EventName": "s3:ObjectCreated:Put",
        "Key": "alexandria-media/218b2504-1736-476e-9975-dc5215ef4f01_test.png",
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "minio:s3",
                "awsRegion": "",
                "eventTime": "2020-07-17T06:38:23.221Z",
                "eventName": "s3:ObjectCreated:Put",
                "userIdentity": {"principalId": "minio"},
                "requestParameters": {
                    "accessKey": "minio",
                    "region": "",
                    "sourceIPAddress": "172.20.0.1",
                },
                "responseElements": {
                    "x-amz-request-id": "162276DB8350E531",
                    "x-minio-deployment-id": "5db7c8da-79cb-4d3a-8d40-189b51ca7aa6",
                    "x-minio-origin-endpoint": "http://172.20.0.2:9000",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "Config",
                    "bucket": {
                        "name": "alexandria-media",
                        "ownerIdentity": {"principalId": "minio"},
                        "arn": "arn:aws:s3:::alexandria-media",
                    },
                    "object": {
                        "key": "218b2504-1736-476e-9975-dc5215ef4f01_test.png",
                        "size": 299758,
                        "eTag": "af1421c17294eed533ec99eb82b468fb",
                        "contentType": "application/pdf",
                        "userMetadata": {"content-variant": "application/pdf"},
                        "versionId": "1",
                        "sequencer": "162276DB83A9F895",
                    },
                },
                "source": {
                    "host": "172.20.0.1",
                    "port": "",
                    "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.0 Chrome/80.0.3987.163 Safari/537.36",
                },
            }
        ],
    }

    settings.ALEXANDRIA_ENABLE_CHECKSUM = enabled
    settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION = False

    document = document_factory()
    file = File.objects.create(
        document=document, name="test.png", pk="218b2504-1736-476e-9975-dc5215ef4f01"
    )

    resp = admin_client.post(reverse("hook"), data=data)
    assert resp.status_code == status_code

    if status_code == HTTP_201_CREATED:
        file.refresh_from_db()

        assert (
            file.checksum
            == "sha256:778caf7d8d81a7ff8041003ef01afe00a85750d15086a3cb267fd8d23d8dd285"
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("created_at", "test"),
        ("created_by_user", "test"),
        ("created_by_group", "test"),
    ],
)
def test_base_read_only(admin_client, document_factory, field, value):
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

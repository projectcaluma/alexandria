import io

import pytest
from django.core.files.base import ContentFile
from django.urls import reverse
from generic_permissions.config import ObjectPermissionsConfig, PermissionsConfig
from generic_permissions.permissions import object_permission_for, permission_for
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from alexandria.core.factories import FileData
from alexandria.core.models import Document, File

TIMESTAMP = "2017-05-21T11:25:41.123840Z"


@pytest.mark.freeze_time(TIMESTAMP)
@pytest.mark.parametrize(
    "method,status",
    [
        ("post", HTTP_201_CREATED),
        ("patch", HTTP_200_OK),
        ("delete", HTTP_204_NO_CONTENT),
    ],
)
@pytest.mark.parametrize("use_admin_client", [True, False])
def test_document_permission(
    document_factory,
    admin_user,
    admin_client,
    client,
    document_post_data,
    method,
    status,
    use_admin_client,
    reset_config_classes,
):
    client = admin_client if use_admin_client else client

    class CustomPermission:
        @permission_for(Document)
        def has_permission_for_document(self, request, *args, **kwargs):
            if request.method == "PATCH":
                return request.data["title"] == "new"
            elif request.method in {"DELETE", "POST"}:
                return request.user.username == "admin"

        @object_permission_for(Document)
        def has_object_permission_for_document(
            self, request, instance, *args, **kwargs
        ):
            assert isinstance(instance, Document)
            if request.user.username == "admin":
                return True
            return False

    PermissionsConfig.register_handler_class(CustomPermission)
    ObjectPermissionsConfig.register_handler_class(CustomPermission)

    doc = document_factory(title="bar")

    url = reverse("document-list")

    if method in ["patch", "delete"]:
        url = reverse("document-detail", args=[doc.pk])

    data = {
        "post": document_post_data,
        "patch": {
            "data": {
                "id": doc.pk,
                "type": "documents",
                "attributes": {"title": "new"},
                "relationships": {
                    "category": {"data": {"id": doc.category.pk, "type": "categories"}}
                },
            }
        },
        "delete": None,
    }

    response = getattr(client, method)(
        url, data=data[method], format="multipart" if method == "post" else None
    )

    if not use_admin_client:
        assert response.status_code == HTTP_403_FORBIDDEN
        return

    assert response.status_code == status
    if method == "post":
        result = response.json()
        assert result["data"]["attributes"]["created-at"] == TIMESTAMP
    elif method == "patch":
        doc.refresh_from_db()
        assert doc.title == "new"


@pytest.mark.freeze_time(TIMESTAMP)
@pytest.mark.parametrize(
    "method,use_admin_client,allow_delete,status",
    [
        ("post", True, False, HTTP_201_CREATED),
        ("post", False, False, HTTP_403_FORBIDDEN),
        ("patch", True, False, HTTP_405_METHOD_NOT_ALLOWED),
        ("patch", False, False, HTTP_403_FORBIDDEN),
        ("delete", True, True, HTTP_204_NO_CONTENT),
        ("delete", False, True, HTTP_403_FORBIDDEN),
    ],
)
def test_file_permission(
    db,
    reset_config_classes,
    admin_user,
    file_factory,
    admin_client,
    client,
    document,
    method,
    use_admin_client,
    status,
    allow_delete,
):
    client = admin_client if use_admin_client else client

    class CustomPermission:
        @permission_for(File)
        def has_permission_for_document(self, request, *args, **kwargs):
            if request.user.username == "admin" or allow_delete:
                return True
            return False

        @object_permission_for(File)
        def has_object_permission_for_document(
            self, request, instance, *args, **kwargs
        ):
            assert isinstance(instance, File)
            if request.user.username == "admin" and allow_delete:
                return True
            return False

    PermissionsConfig.register_handler_class(CustomPermission)
    ObjectPermissionsConfig.register_handler_class(CustomPermission)

    file = file_factory(name="bar")

    url = reverse("file-list")

    data = {
        "name": "image.png",
        "document": str(document.pk),
        "content": io.BytesIO(FileData.png),
        "variant": File.Variant.ORIGINAL,
    }

    if method in ["patch", "delete"]:
        url = reverse("file-detail", args=[file.pk])
        data["id"] = str(file.pk)

    if method == "patch":
        data["name"] = "new"

    response = getattr(client, method)(url, data=data, format="multipart")

    assert response.status_code == status
    if method == "post" and use_admin_client:
        result = response.json()
        assert result["data"]["attributes"]["created-at"] == TIMESTAMP


@pytest.mark.parametrize(
    "use_admin_client,status",
    [
        (True, HTTP_200_OK),
        (False, HTTP_403_FORBIDDEN),
    ],
)
def test_webdav_permission(
    manabi,
    document_factory,
    admin_user,
    admin_client,
    client,
    status,
    use_admin_client,
    file_factory,
    reset_config_classes,
):
    client = admin_client if use_admin_client else client

    class CustomPermission:
        @permission_for(Document)
        def has_permission_for_document(self, request, *args, **kwargs):
            return request.user.username == "admin"

        @object_permission_for(Document)
        def has_object_permission_for_document(
            self, request, instance, *args, **kwargs
        ):
            return request.user.username == "admin"

    PermissionsConfig.register_handler_class(CustomPermission)
    ObjectPermissionsConfig.register_handler_class(CustomPermission)

    document = document_factory(title="bar")
    content_file = ContentFile(b"hello world", name="test.txt")
    file = file_factory(
        name="test.txt",
        content=content_file,
        size=content_file.size,
        mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    document.files.add(file)

    url = reverse("webdav-detail", args=[document.pk])

    response = client.get(url)

    assert response.status_code == status

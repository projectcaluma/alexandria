import io

import pytest
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
    method,
    status,
    use_admin_client,
    reset_config_classes,
):
    client = admin_client if use_admin_client else client

    class CustomPermission:
        @permission_for(Document)
        def has_permission_for_document(self, request):
            if request.user.username == "admin" or request.data["title"]["en"] == "new":
                return True
            return False

        @object_permission_for(Document)
        def has_object_permission_for_document(self, request, instance):
            assert isinstance(instance, Document)
            if request.user.username == "admin":
                return True
            return False

    PermissionsConfig.register_handler_class(CustomPermission)
    ObjectPermissionsConfig.register_handler_class(CustomPermission)

    doc = document_factory(title="bar")

    url = reverse("document-list")

    data = {
        "data": {
            "type": "documents",
            "attributes": {"title": {"de": "", "en": "foo", "fr": ""}},
        }
    }

    if method in ["patch", "delete"]:
        url = reverse("document-detail", args=[doc.pk])
        data["data"]["id"] = str(doc.pk)

    if method == "patch":
        data["data"]["attributes"]["title"] = {
            "de": "",
            "en": "new",
            "fr": "",
        }

    response = getattr(client, method)(url, data=data)

    if not use_admin_client:
        assert response.status_code == HTTP_403_FORBIDDEN
        return

    assert response.status_code == status
    if method == "post":
        result = response.json()
        assert result["data"]["attributes"]["created-at"] == TIMESTAMP
    elif method == "patch":
        doc.refresh_from_db()
        assert doc.title["en"] == "new"


@pytest.mark.freeze_time(TIMESTAMP)
@pytest.mark.parametrize(
    "method,use_admin_client,allow_delete,status",
    [
        ("post", True, False, HTTP_201_CREATED),
        ("post", False, False, HTTP_403_FORBIDDEN),
        ("patch", True, False, HTTP_405_METHOD_NOT_ALLOWED),
        ("patch", False, False, HTTP_405_METHOD_NOT_ALLOWED),
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
        def has_permission_for_document(self, request):
            if request.user.username == "admin" or allow_delete:
                return True
            return False

        @object_permission_for(File)
        def has_object_permission_for_document(self, request, instance):
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

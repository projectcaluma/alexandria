import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from alexandria.core.models import Document, File, PermissionMixin, Tag
from alexandria.core.permissions import (
    BasePermission,
    IsAuthenticated,
    object_permission_for,
    permission_for,
)

TIMESTAMP = "2017-05-21T11:25:41.123840Z"


@pytest.fixture
def reset_permission_classes():
    before = PermissionMixin.permission_classes
    yield
    PermissionMixin.permission_classes = before


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
def test_permission(
    document_factory,
    admin_user,
    admin_client,
    client,
    method,
    status,
    use_admin_client,
    reset_permission_classes,
):
    client = admin_client if use_admin_client else client

    class CustomPermission(BasePermission):
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

    PermissionMixin.permission_classes = [CustomPermission]

    doc = document_factory(title="bar")

    url = reverse("document-list")

    data = {
        "data": {
            "variant": "documents",
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


def test_permission_no_permissions_configured(client, reset_permission_classes):
    PermissionMixin.permission_classes = None

    data = {
        "data": {
            "variant": "documents",
            "attributes": {"title": {"de": "", "en": "foo", "fr": ""}},
        }
    }

    url = reverse("document-list")
    with pytest.raises(ImproperlyConfigured):
        client.post(url, data=data)


def test_custom_permission_override_has_permission_with_duplicates():
    class CustomPermission(BasePermission):
        @permission_for(Document)
        def has_permission_for_custom_mutation(self, request):  # pragma: no cover
            return False

        @permission_for(Document)
        def has_permission_for_custom_mutation_2(self, request):  # pragma: no cover
            return False

    with pytest.raises(ImproperlyConfigured):
        CustomPermission()


def test_custom_permission_override_has_object_permission_with_duplicates():
    class CustomPermission(BasePermission):
        @object_permission_for(Document)
        def has_object_permission_for_custom_mutation(
            self, request, instance
        ):  # pragma: no cover
            return False

        @object_permission_for(Document)
        def has_object_permission_for_custom_mutation_2(
            self, request, instance
        ):  # pragma: no cover
            return False

    with pytest.raises(ImproperlyConfigured):
        CustomPermission()


def test_custom_permission_override_has_permission_with_multiple_models(request):
    class CustomPermission(BasePermission):
        @permission_for(Document)
        @permission_for(Tag)
        def has_permission_for_both_mutations(self, request):  # pragma: no cover
            return False

    assert not CustomPermission().has_permission(Document, request)
    assert not CustomPermission().has_permission(Tag, request)


def test_custom_permission_override_has_object_permission_with_multiple_mutations(
    db, request, document, tag
):
    class CustomPermission(BasePermission):
        @object_permission_for(Document)
        @object_permission_for(Tag)
        def has_object_permission_for_both_mutations(
            self, request, instance
        ):  # pragma: no cover
            return False

    assert not CustomPermission().has_object_permission(Document, request, document)
    assert not CustomPermission().has_object_permission(Tag, request, tag)


@pytest.mark.parametrize(
    "authenticated, expect_permission", [(True, True), (False, False)]
)
def test_authenticated_permission(
    db, document, authenticated, expect_permission, mocker, user
):
    request = mocker.MagicMock()
    request.user = user if authenticated else AnonymousUser()

    permissions = IsAuthenticated()
    perms = [
        permissions.has_permission(Document, request),
        permissions.has_object_permission(Document, request, document),
        permissions.has_permission(Tag, request),
        permissions.has_object_permission(Tag, request, document),
        permissions.has_permission(File, request),
        permissions.has_object_permission(File, request, document),
    ]
    assert perms == [expect_permission for _ in perms]

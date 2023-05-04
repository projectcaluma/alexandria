import pytest
from django.apps import apps
from django.urls import reverse
from generic_permissions.config import VisibilitiesConfig
from generic_permissions.visibilities import filter_queryset_for
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from alexandria.core.models import Document
from alexandria.oidc_auth.authentication import OIDCUser


@pytest.mark.parametrize("detail", [True, False])
@pytest.mark.parametrize("use_admin_client", [True, False])
def test_visibility(
    reset_config_classes,
    document_factory,
    admin_user,
    admin_client,
    client,
    detail,
    use_admin_client,
):
    client = admin_client if use_admin_client else client

    class TestVisibility:
        @filter_queryset_for(Document)
        def filter_queryset_for_document(self, queryset, request):
            if request.user.username != "admin":
                return queryset.none()
            return queryset.exclude(category__slug="bar")

    VisibilitiesConfig.register_handler_class(TestVisibility)

    document = document_factory(category__slug="foo")
    document_factory(category__slug="bar")

    url = reverse("document-list")
    if detail:
        url = reverse("document-detail", args=[document.pk])
    response = client.get(url)
    if detail and not use_admin_client:
        assert response.status_code == HTTP_404_NOT_FOUND
        return
    assert response.status_code == HTTP_200_OK
    result = response.json()
    if not detail:
        if use_admin_client:
            assert len(result["data"]) == 1
            assert result["data"][0]["relationships"]["category"]["data"]["id"] == "foo"
        else:
            assert len(result["data"]) == 0
    else:
        assert result["data"]["relationships"]["category"]["data"]["id"] == "foo"


@pytest.mark.parametrize("requesting_user", ["anon", "user", "admin"])
def test_own_and_admin_visibility(
    db,
    document_factory,
    file_factory,
    request,
    requesting_user,
    user,
    admin_user,
    client,
    settings,
):
    settings.GENERIC_PERMISSIONS_VISIBILITY_CLASSES = [
        "alexandria.core.visibilities.OwnAndAdmin"
    ]
    apps.get_app_config("generic_permissions").ready()

    expected_count = 0
    if requesting_user == "admin":
        client.force_authenticate(
            OIDCUser(token="foo", claims={"sub": admin_user.username})
        )
        expected_count = 2
    elif requesting_user == "user":
        client.force_authenticate(OIDCUser(token="foo", claims={"sub": user.username}))
        expected_count = 1

    file_factory(
        created_by_user=requesting_user, document__created_by_user=requesting_user
    )
    file_factory(created_by_user="admin", document__created_by_user="admin")

    resp = client.get(reverse("document-list"))
    assert len(resp.json()["data"]) == expected_count

    resp = client.get(reverse("file-list"))
    assert len(resp.json()["data"]) == expected_count

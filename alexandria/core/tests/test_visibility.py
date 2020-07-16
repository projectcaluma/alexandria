import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from alexandria.core.models import (
    BaseModel,
    Category,
    Document,
    File,
    Tag,
    VisibilityMixin,
)
from alexandria.core.visibilities import (
    BaseVisibility,
    OwnAndAdmin,
    Union,
    filter_queryset_for,
)


@pytest.mark.parametrize("detail", [True, False])
@pytest.mark.parametrize("use_admin_client", [True, False])
def test_visibility(
    reset_visibilities,
    document_factory,
    admin_user,
    admin_client,
    client,
    detail,
    use_admin_client,
):
    client = admin_client if use_admin_client else client

    class TestVisibility(BaseVisibility):
        @filter_queryset_for(Document)
        def filter_queryset_for_document(self, queryset, request):
            if request.user.username != "admin":
                return queryset.none()
            return queryset.exclude(category__slug="bar")

    VisibilityMixin.visibility_classes = [TestVisibility]

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


def test_visibility_no_visibilities_configured(reset_visibilities, client):
    VisibilityMixin.visibility_classes = None

    url = reverse("document-list")
    with pytest.raises(ImproperlyConfigured):
        client.get(url)


def test_visibility_dupes(reset_visibilities, client):
    class TestVisibility(BaseVisibility):
        @filter_queryset_for(Document)
        def filter_queryset_for_document(self, queryset, request):  # pragma: no cover
            return queryset

        @filter_queryset_for(Document)
        def filter_queryset_for_document2(self, queryset, request):  # pragma: no cover
            return queryset

    VisibilityMixin.visibility_classes = [TestVisibility]

    url = reverse("document-list")
    with pytest.raises(ImproperlyConfigured):
        client.get(url)


def test_custom_visibility_for_basemodel(
    reset_visibilities, db, client, document_factory
):
    """Test fallback to BaseModel."""
    document_factory(category__slug="Cat1")
    document_factory(category__slug="Cat2")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

    VisibilityMixin.visibility_classes = [CustomVisibility]

    assert Document.objects.count() == 2

    url = reverse("document-list")
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    result = response.json()

    assert result == {"data": []}


def test_custom_visibility_override_specificity(db, document_factory):
    """The first matching filter 'wins'."""
    document_factory(category__slug="Cat1")
    document_factory(category__slug="Cat2")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

        @filter_queryset_for(Document)
        def filter_queryset_for_document(self, queryset, request):
            return queryset.filter(category__slug="Cat1")

    assert Document.objects.count() == 2
    queryset = CustomVisibility().filter_queryset(BaseModel, Document.objects, None)
    assert queryset.count() == 0
    queryset = CustomVisibility().filter_queryset(Document, Document.objects, None)
    assert queryset.count() == 1


def test_custom_visibility_chained_decorators(db, category_factory, tag_factory):
    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

        @filter_queryset_for(Category)
        @filter_queryset_for(Tag)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(slug="name1")

    category_factory(slug="name1")
    category_factory(slug="name2")
    tag_factory(slug="name1")
    tag_factory(slug="name2")

    assert Category.objects.count() == 2
    assert Tag.objects.count() == 2
    queryset = CustomVisibility().filter_queryset(BaseModel, Category.objects, None)
    assert queryset.count() == 0
    queryset = CustomVisibility().filter_queryset(Category, Category.objects, None)
    assert queryset.count() == 1
    queryset = CustomVisibility().filter_queryset(Tag, Tag.objects, None)
    assert queryset.count() == 1


def test_union_visibility(db, document_factory):
    document_factory(title="Doc1")
    document_factory(title="Doc2")
    document_factory(title="Doc3")
    document_factory(title="Doc4")

    class Name1Visibility(BaseVisibility):
        @filter_queryset_for(Document)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(title__en="Doc1")

    class Name2Visibility(BaseVisibility):
        @filter_queryset_for(Document)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(title__en="Doc2")

    class Name3Visibility(BaseVisibility):
        @filter_queryset_for(Document)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(title__en__in=["Doc2", "Doc3"])

    class ConfiguredUnion(Union):
        visibility_classes = [Name1Visibility, Name2Visibility, Name3Visibility]

    queryset = Document.objects
    result = Name1Visibility().filter_queryset(Document, queryset, None)
    assert result.count() == 1
    result = Name2Visibility().filter_queryset(Document, queryset, None)
    assert result.count() == 1
    result = Name3Visibility().filter_queryset(Document, queryset, None)
    assert result.count() == 2
    queryset = ConfiguredUnion().filter_queryset(Document, queryset, None)
    assert queryset.count() == 3
    assert queryset.get(title__en="Doc2")


def test_union_visibility_none(db, document_factory):
    document_factory(title="Doc1")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(Document)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.none()

    class CustomVisibility2(BaseVisibility):
        @filter_queryset_for(Document)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.none()

    class ConfiguredUnion(Union):
        visibility_classes = [CustomVisibility2, CustomVisibility]

    queryset = Document.objects
    result = CustomVisibility().filter_queryset(Document, queryset, None)
    assert result.count() == 0
    result = CustomVisibility2().filter_queryset(Document, queryset, None)
    assert result.count() == 0
    queryset = ConfiguredUnion().filter_queryset(Document, queryset, None)
    assert queryset.count() == 0


@pytest.mark.parametrize("requesting_user", ["anon", "user", "admin"])
def test_own_and_admin_visibility(
    db, document_factory, file_factory, request, requesting_user, user, admin_user,
):
    request.user = AnonymousUser()
    expected_count = 0
    if requesting_user == "admin":
        request.user = admin_user
        expected_count = 2
    elif requesting_user == "user":
        request.user = user
        expected_count = 1

    file_factory(
        created_by_user=requesting_user, document__created_by_user=requesting_user
    )
    file_factory(created_by_user="admin", document__created_by_user="admin")

    result = OwnAndAdmin().filter_queryset(Document, Document.objects, request)
    assert result.count() == expected_count

    result = OwnAndAdmin().filter_queryset(File, File.objects, request)
    assert result.count() == expected_count

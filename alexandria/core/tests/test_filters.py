import json

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from ..views import CategoryViewSet, DocumentViewSet, FileViewSet, TagViewSet


@pytest.mark.parametrize(
    "value,status_code",
    [
        (json.dumps([{"key": "foo", "value": "bar"}]), HTTP_200_OK),
        (json.dumps([{"key": "int", "value": 5, "lookup": "gt"}]), HTTP_200_OK),
        (
            json.dumps(
                [{"key": "foo", "value": "bar"}, {"key": "baz", "value": "bla"}]
            ),
            HTTP_200_OK,
        ),
        (
            json.dumps([{"key": "foo", "value": "ar", "lookup": "contains"}]),
            HTTP_200_OK,
        ),
        (
            json.dumps([{"key": "foo", "value": "bar", "lookup": "asdfgh"}]),
            HTTP_400_BAD_REQUEST,
        ),
        (json.dumps([{"key": "foo"}]), HTTP_400_BAD_REQUEST),
        (json.dumps({"key": "foo"}), HTTP_400_BAD_REQUEST),
        ("foo", HTTP_400_BAD_REQUEST),
        ("[{foo, no json)", HTTP_400_BAD_REQUEST),
    ],
)
def test_json_value_filter(db, document_factory, admin_client, value, status_code):
    doc = document_factory(meta={"foo": "bar", "baz": "bla", "int": 23})
    document_factory(meta={"foo": "baz"})
    document_factory()
    url = reverse("document-list")
    resp = admin_client.get(url, {"filter[meta]": value})
    assert resp.status_code == status_code
    if status_code == HTTP_200_OK:
        result = resp.json()
        assert len(result["data"]) == 1
        assert result["data"][0]["id"] == str(doc.pk)


@pytest.mark.parametrize(
    "value,amount",
    [
        ("foo_tag", 1),
        ("_t", 2),
        ("foo_title", 1),
        ("filename.pdf", 1),
        ("filename", 2),
    ],
)
def test_document_search_filter(
    db, document_factory, tag_factory, file_factory, admin_client, value, amount
):
    """
    Test document search filter.

    This test makes sure that search lookups are restricted to the current language.
    """
    tag1 = tag_factory(name="bar_tag")  # matches
    tag2 = tag_factory(name="foo_tag")  # doesn't match
    doc = document_factory(title={"en": "foo_title", "de": "bar_title"})  # matches
    doc2 = document_factory(
        title={"en": "bar_title", "de": "foo_title"}
    )  # doesn't match
    doc.tags.add(tag1)
    doc2.tags.add(tag2)
    file_factory(name="filename.pdf", document=doc)
    file_factory(name="filename2.pdf", document=doc2)
    document_factory()
    url = reverse("document-list")
    resp = admin_client.get(url, {"filter[search]": value})
    assert resp.status_code == HTTP_200_OK

    result = resp.json()
    assert len(result["data"]) == amount


def test_tag_category_filter(db, document_factory, tag_factory, admin_client):
    blue = tag_factory(slug="blue")
    red = tag_factory(slug="red")
    green = tag_factory(slug="green")
    doc1 = document_factory(category__slug="cat1")
    doc1.tags.add(blue)
    doc2 = document_factory(category_id="cat1")
    doc2.tags.add(green)
    doc3 = document_factory(category__slug="cat2")
    doc3.tags.add(red)

    # one more to test distinctiveness of the result
    doc4 = document_factory(category_id="cat1")
    doc4.tags.add(blue)

    url = reverse("tag-list")
    resp = admin_client.get(url, {"filter[with-documents-in-category]": "cat1"})
    assert resp.status_code == HTTP_200_OK
    result = resp.json()
    assert len(result["data"]) == 2

    returned_tags = [tag["id"] for tag in result["data"]]
    assert sorted(returned_tags) == sorted(["blue", "green"])


@pytest.mark.parametrize(
    "tag_filter, expect_documents",
    [
        ("blue", ["doc1"]),
        ("green", ["doc1", "doc2"]),
        ("green,red", ["doc2"]),
        ("pink,green", ["doc1"]),
    ],
)
def test_tag_filter(
    db, document_factory, tag_factory, tag_filter, expect_documents, admin_client
):
    blue = tag_factory(slug="blue")
    red = tag_factory(slug="red")
    green = tag_factory(slug="green")
    pink = tag_factory(slug="pink")

    doc1 = document_factory()
    doc1.tags.add(blue)
    doc1.tags.add(green)
    doc1.tags.add(pink)
    doc2 = document_factory()
    doc2.tags.add(red)
    doc2.tags.add(green)

    documents = {"doc1": doc1, "doc2": doc2}

    url = reverse("document-list")
    resp = admin_client.get(url, {"filter[tags]": tag_filter})
    assert resp.status_code == HTTP_200_OK
    result = resp.json()
    received_ids = set([obj["id"] for obj in result["data"]])
    expected_ids = set([str(documents[doc].pk) for doc in expect_documents])
    assert received_ids == expected_ids


@pytest.mark.parametrize(
    "admin_groups, active_group, expect_failure",
    [
        (["foo", "bar"], "foo", False),
        (["foo", "bar"], None, False),
        (["foo", "bar"], "somethingelse", True),
    ],
)
@pytest.mark.parametrize(
    "viewset", [CategoryViewSet, DocumentViewSet, FileViewSet, TagViewSet]
)
def test_active_group_filter(
    db, viewset, request, admin_client, active_group, expect_failure
):
    viewset_inst = viewset()
    model_name = viewset_inst.queryset.model.__name__.lower()
    records = request.getfixturevalue(f"{model_name}_factory").create_batch(2)
    url = reverse(f"{model_name}-list")

    filter = {"filter[activeGroup]": active_group} if active_group is not None else {}

    if expect_failure:
        # with pytest.raises(ValidationError):
        response = admin_client.get(url, filter)
        assert response.status_code == HTTP_400_BAD_REQUEST

    else:
        response = admin_client.get(url, filter)
        # we expect no filtering
        assert response.status_code == HTTP_200_OK
        # >= as there might be leftovers from other tests (shouldn't but may happen.)
        # Important is that the filter doesn't LIMIT its output
        assert len(response.json()["data"]) >= len(records)


@pytest.mark.parametrize(
    "mangle",
    [
        lambda name: name.lower(),
        lambda name: name.upper(),
        lambda name: name.lower()[:-3],
        lambda name: name.lower()[:-3],
        lambda name: name.upper()[:-3],
    ],
)
def test_tag_search(db, tag_factory, mangle, admin_client):
    tags = tag_factory.create_batch(4)

    search = mangle(tags[0].name)

    url = reverse("tag-list")
    resp = admin_client.get(url, {"filter[name]": search})
    assert resp.status_code == HTTP_200_OK
    result = resp.json()

    received_ids = set([obj["id"] for obj in result["data"]])
    assert str(tags[0].pk) in received_ids

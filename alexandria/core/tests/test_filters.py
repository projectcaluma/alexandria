import json

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


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
    tag1 = tag_factory(name={"en": "foo_tag", "de": "bar_tag"})  # matches
    tag2 = tag_factory(name={"en": "bar_tag", "de": "foo_tag"})  # doesn't match
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

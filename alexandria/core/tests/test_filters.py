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

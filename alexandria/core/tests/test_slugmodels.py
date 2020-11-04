"""Module to test api in a generic way."""

import pytest
from django.urls import reverse


@pytest.mark.freeze_time("2017-05-21")
def test_create_tags(admin_client):
    url = reverse("tag-list")
    # create multiple to ensure PK generation works
    for name in ["foo", "bar", "baz"]:
        name_en = name[::-1]
        payload = {
            "data": {
                "attributes": {"name": {"de": name, "en": name_en}, "slug": name},
                "type": "tags",
            }
        }

        resp = admin_client.post(url, payload)

        assert resp.status_code == 201
        assert resp.json() == {
            "data": {
                "type": "tags",
                "id": name_en,
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-user": None,
                    "created-by-group": None,
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-user": "admin",
                    "modified-by-group": "admin",
                    "meta": {},
                    "name": {"de": name, "en": name_en, "fr": ""},
                    "description": {"en": "", "de": "", "fr": ""},
                },
            }
        }

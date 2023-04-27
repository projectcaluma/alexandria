import pytest
from django.urls import reverse


@pytest.mark.freeze_time("2017-05-21")
@pytest.mark.parametrize("admin_groups", [["foo"]])
def test_create_tags(admin_client):
    url = reverse("tag-list")
    # create multiple to ensure PK generation works
    for name in ["foo", "bar", "baz"]:
        payload = {"data": {"attributes": {"name": name, "slug": name}, "type": "tags"}}

        resp = admin_client.post(url, payload)

        assert resp.status_code == 201
        assert resp.json() == {
            "data": {
                "type": "tags",
                "id": name,
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "created-by-user": "admin",
                    "created-by-group": "foo",
                    "modified-at": "2017-05-21T00:00:00Z",
                    "modified-by-user": "admin",
                    "modified-by-group": "foo",
                    "metainfo": {},
                    "name": name,
                    "description": {"en": "", "de": "", "fr": ""},
                },
                "relationships": {"tag-synonym-group": {"data": None}},
            }
        }

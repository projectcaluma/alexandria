"""Module to test api in a generic way."""

import hashlib
import io
import json
import re
import uuid

import inflection
import pytest
from django.db import connection
from django.db.models.fields.related import ManyToManyDescriptor
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework_json_api.renderers import JSONRenderer

from ..views import (
    CategoryViewSet,
    DocumentViewSet,
    FileViewSet,
    MarkViewSet,
    TagViewSet,
)


@pytest.fixture
def disable_relationship_visibilities(settings):
    settings.GENERIC_PERMISSIONS_BYPASS_VISIBILITIES = {
        "alexandria_core.Category": "__all__",
        "alexandria_core.Document": "__all__",
        "alexandria_core.File": "__all__",
        "alexandria_core.Mark": "__all__",
        "alexandria_core.Tag": "__all__",
        "alexandria_core.TagSynonymGroup": "__all__",
    }


@pytest.fixture()
def deterministic_uuids(mocker):
    # md5 hex digests are the same length as UUIDs, so django happily accepts
    # them.  Note also this has no cryptographic use here, so md5 is totally
    # fine
    hashy = hashlib.md5()

    def next_uuid():
        # add some string to the hash. This modifies it enough to yield a
        # totally different value
        hashy.update(b"x")
        # format: 9336ebf2-5087-d91c-818e-e6e9 ec29 f8c1
        # lengths: 8        4    4    4    12
        digest = hashy.hexdigest()
        return uuid.UUID(
            "-".join(
                [
                    digest[:8],  # 8
                    digest[8:12],  # 4
                    digest[12:16],  # 4
                    digest[16:20],  # 4
                    digest[20:],  # 4
                ]
            )
        )

    mocker.patch("uuid.uuid4", next_uuid)


@pytest.fixture(
    params=[
        # add your viewset and expected queries run for generic api testing...
        CategoryViewSet,
        DocumentViewSet,
        FileViewSet,
        TagViewSet,
        MarkViewSet,
    ]
)
def viewset(request, disable_relationship_visibilities):
    """
    Viewset fixture listing viewsets for generic testing.

    For generic testing viewset needs to meet following requirements:
    * class fields `serializer_class` and `queryset`
    * registered factory for model it serves
    * registered uri with `SimpleRouter`
    """
    viewset_instance = request.param()
    model = viewset_instance.queryset.model
    factory_name = inflection.underscore(model._meta.object_name)
    base_name = model._meta.object_name.lower()

    viewset_instance.factory_name = factory_name
    viewset_instance.base_name = base_name
    viewset_instance.kwargs = {}

    return viewset_instance


@pytest.fixture
def fixture(
    deterministic_uuids,
    django_db_reset_sequences,
    request,
    viewset,
):
    """Get fixture and many to many relations of given viewset."""
    fixture = request.getfixturevalue(viewset.factory_name)
    included = (
        viewset.serializer_class.included_serializers
        if hasattr(viewset.serializer_class, "included_serializers")
        else {}
    )
    for name in sorted(included.keys()):
        relation_type = getattr(fixture.__class__, name)
        # pytest factory boy doesn't have native ManyToMany support
        # so needs to be handled manually
        if isinstance(relation_type, ManyToManyDescriptor):
            print("{0}_{1}".format(viewset.factory_name, name))
            request.getfixturevalue("{0}_{1}".format(viewset.factory_name, name))

    return fixture


def prefetch_query_in_normalizer(query):
    """
    Normalize `IN` queries.

    Using `prefetch_related()` leads to `IN` queries where we have no control over the
    order of the parameters. Make sure the order in the snapshot is always
    alphabetical.
    """
    regex = r".* IN \((.*)\).*"
    match = re.match(regex, query)
    if match and match.groups():
        for group in match.groups():
            lst = group.split(", ")
            new_string = ", ".join(sorted(lst))
            query = query.replace(group, new_string)
    return query


def assert_response(
    response, query_context, snapshot, *, request_payload=None, include_json=True
):
    value = {
        "status": response.status_code,
        "query_count": len(query_context.captured_queries),
        "queries": [
            prefetch_query_in_normalizer(query["sql"])
            for query in query_context.captured_queries
        ],
        "request": {
            k: v for k, v in response.request.items() if not k.startswith("wsgi")
        },
        "request_payload": request_payload if request_payload else None,
    }

    # Drop `SAVEPOINT` statements because they will change on every run.
    value["queries"] = list(
        filter(lambda lst: "SAVEPOINT" not in lst, value["queries"])
    )

    if include_json:
        value["response"] = response.json()

    assert value == snapshot


@pytest.mark.freeze_time("2017-05-21")
def test_api_list(fixture, request, admin_client, snapshot, viewset):
    url = reverse("{0}-list".format(viewset.base_name))

    # create more data for proper num queries check
    request.getfixturevalue(viewset.factory_name + "_factory").create_batch(2)

    included = getattr(viewset.serializer_class, "included_serializers", {})
    with CaptureQueriesContext(connection) as context:
        response = admin_client.get(url, data={"include": ",".join(included.keys())})

    assert_response(response, context, snapshot)


@pytest.mark.freeze_time("2017-05-21")
def test_api_detail(fixture, admin_client, viewset, snapshot):
    url = reverse("{0}-detail".format(viewset.base_name), args=[fixture.pk])

    included = getattr(viewset.serializer_class, "included_serializers", {})
    with CaptureQueriesContext(connection) as context:
        response = admin_client.get(url, data={"include": ",".join(included.keys())})

    if viewset.get_view_name() == "File":
        content = response.json()
        content["data"]["attributes"]["content"] = io.BytesIO(b"somefilecontent")
        response.content = content

    assert_response(response, context, snapshot)


@pytest.mark.freeze_time("2017-05-21")
def test_api_create(fixture, admin_client, viewset, snapshot, document_post_data):
    url = reverse("{0}-list".format(viewset.base_name))

    serializer = viewset.serializer_class(fixture)
    renderer = JSONRenderer()
    context = {"view": viewset}
    serializer_data = serializer.data
    data = json.loads(renderer.render(serializer_data, renderer_context=context))
    fixture.delete()  # avoid constraint issues

    opts = {}

    if viewset.get_view_name() == "File":
        data = {
            "content": io.BytesIO(b"FiLeCoNtEnt"),
            "name": "foo.txt",
            "document": str(fixture.document.pk),
        }
        opts = {"format": "multipart"}
    elif viewset.get_view_name() == "Document":
        data = document_post_data
        opts = {"format": "multipart"}

    with CaptureQueriesContext(connection) as context:
        response = admin_client.post(url, data=data, **opts)

    assert_response(response, context, snapshot, request_payload=data)


@pytest.mark.freeze_time("2017-05-21")
def test_api_patch(fixture, admin_client, viewset, snapshot):
    url = reverse("{0}-detail".format(viewset.base_name), args=[fixture.pk])
    if viewset.get_view_name() == "File":
        return
    serializer = viewset.serializer_class(fixture)
    renderer = JSONRenderer()
    context = {"view": viewset}
    data = json.loads(renderer.render(serializer.data, renderer_context=context))

    with CaptureQueriesContext(connection) as context:
        response = admin_client.patch(url, data=data)
    assert_response(response, context, snapshot, request_payload=data)


@pytest.mark.freeze_time("2017-05-21")
def test_api_destroy(fixture, admin_client, snapshot, viewset):
    url = reverse("{0}-detail".format(viewset.base_name), args=[fixture.pk])

    with CaptureQueriesContext(connection) as context:
        response = admin_client.delete(url)

    assert_response(response, context, snapshot, include_json=False)

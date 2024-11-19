import pytest
import tika.parser
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
)


@pytest.fixture
def searchable_data(
    db, settings, django_assert_num_queries, document_factory, file_factory, mocker
):
    settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH = True
    doc1 = document_factory(title="Apple")
    doc2 = document_factory(title="Pear")

    mocker.patch("tika.parser.from_buffer", return_value={"content": "Important text"})
    file_factory(document=doc1, name="Paris.png", mime_type="image/png")

    mocker.patch("tika.parser.from_buffer", return_value={"content": "Title text"})
    file_factory(document=doc1, name="London.png", mime_type="image/png")

    mocker.patch("tika.parser.from_buffer", return_value={"content": "Hidden"})
    file_factory(document=doc2, name="Athens.jpeg", mime_type="image/jpeg")

    mocker.patch("tika.parser.from_buffer", return_value={"content": "Important text"})
    tika.parser.from_buffer.return_value = {"content": "Important text"}
    file_factory(document=doc2, name="Bern.jpeg", mime_type="image/jpeg")

    return doc1, doc2


@pytest.mark.parametrize(
    "filters,expected_name,num_queries",
    [
        (
            {"filter[query]": "important"},
            {"Bern.jpeg", "Paris.png"},
            1,
        ),
        ({"filter[query]": "London"}, {"London.png"}, 1),
    ],
)
def test_file_search(
    db,
    settings,
    django_assert_num_queries,
    document_factory,
    file_factory,
    admin_client,
    filters,
    expected_name,
    num_queries,
    searchable_data,
):
    doc1, doc2 = searchable_data

    assert doc1.files.count() == 4
    assert doc2.files.count() == 4

    with django_assert_num_queries(num_queries):
        response = admin_client.get(reverse("search-list"), filters)

    assert response.status_code == HTTP_200_OK
    data = response.json()["data"]

    assert data[0]["type"] == "search-results"
    assert {result["attributes"]["file-name"] for result in data} == expected_name


def test_search_empty(db, django_assert_num_queries, admin_client, searchable_data):
    doc1, doc2 = searchable_data

    with django_assert_num_queries(0):
        response = admin_client.get(reverse("search-list"))

    assert response.status_code == HTTP_200_OK
    data = response.json()["data"]
    assert data == []

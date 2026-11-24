import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


@pytest.fixture
def stamp_mark(mark_factory, category_factory):
    decision = category_factory(slug="decision-documents")
    mark = mark_factory(slug="stamp", metainfo={"categories": [decision.pk]})
    return mark, decision


def _patch(client, document, **relationships):
    return client.patch(
        reverse("document-detail", args=[document.pk]),
        {
            "data": {
                "type": "documents",
                "id": str(document.pk),
                "relationships": relationships,
            }
        },
    )


@pytest.mark.django_db
@pytest.mark.parametrize("in_allowed_category", [True, False])
def test_set_limited_mark(
    admin_client, document_factory, category_factory, stamp_mark, in_allowed_category
):
    mark, decision = stamp_mark
    # Descendants of the allowed category are allowed too
    grandchild = category_factory(parent=category_factory(parent=decision))
    document = document_factory(
        category=grandchild if in_allowed_category else category_factory()
    )

    response = _patch(
        admin_client,
        document,
        marks={"data": [{"type": "marks", "id": mark.pk}]},
    )

    expected = HTTP_200_OK if in_allowed_category else HTTP_400_BAD_REQUEST
    assert response.status_code == expected, response.json()


@pytest.mark.django_db
def test_move_rejected_with_limited_mark(
    admin_client, document_factory, category_factory, stamp_mark
):
    mark, decision = stamp_mark
    document = document_factory(category=decision)
    document.marks.add(mark)

    response = _patch(
        admin_client,
        document,
        category={"data": {"type": "categories", "id": category_factory().pk}},
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    document.refresh_from_db()
    assert document.category == decision


@pytest.mark.django_db
def test_unlimited_mark(admin_client, document_factory, mark_factory):
    document = document_factory()

    response = _patch(
        admin_client,
        document,
        marks={"data": [{"type": "marks", "id": mark_factory().pk}]},
    )

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_limited_mark_single_slug(mark_factory, category_factory):
    decision = category_factory(slug="decision-documents")
    # Not a list, must not match parts of a slug
    part = category_factory(slug="decision")
    mark = mark_factory(metainfo={"categories": decision.pk})

    assert mark.allows_category(decision)
    assert not mark.allows_category(part)

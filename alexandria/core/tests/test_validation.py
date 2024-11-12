from collections import Counter

from django.urls import reverse
from generic_permissions.config import ValidatorsConfig
from generic_permissions.validation import validator_for

from alexandria.core.models import Tag


def test_custom_validation(db, reset_config_classes, tag, file, admin_client):
    call_counter = Counter()

    class TestValidator:
        @validator_for(Tag)
        def validate(self, data, context):
            data["created_by_group"] = "foobar"
            call_counter["validate"] += 1
            # Ensure serializer is available and functional
            assert context["request"].method == "PATCH"
            return data

    ValidatorsConfig.register_handler_class(TestValidator)

    url = reverse("tag-detail", args=[tag.pk])

    # first, ensure validator is called for Document
    admin_client.patch(url, json={})
    assert call_counter["validate"] == 1

    # See if the validation had some effect
    tag.refresh_from_db()
    assert tag.created_by_group == "foobar"

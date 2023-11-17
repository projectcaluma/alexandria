from collections import Counter

from django.urls import reverse
from generic_permissions.config import ValidatorsConfig
from generic_permissions.validation import validator_for

from alexandria.core.models import Document


def test_validation(db, reset_config_classes, document, file, admin_client):
    call_counter = Counter()

    class TestValidator:
        @validator_for(Document)
        def validate(self, data, context):
            data["created_by_group"] = "foobar"
            call_counter["validate"] += 1
            # Ensure serializer is available and functional
            assert context["request"].method == "PATCH"
            return data

    ValidatorsConfig.register_handler_class(TestValidator)

    url = reverse("document-detail", args=[document.pk])

    # first, ensure validator is called for Document
    admin_client.patch(url, json={})
    assert call_counter["validate"] == 1

    # See if the validation had some effect
    document.refresh_from_db()
    assert document.created_by_group == "foobar"

    # second, ensure validator is not called for File
    url = reverse("file-detail", args=[file.pk])
    admin_client.patch(url, json={})
    assert call_counter["validate"] == 1

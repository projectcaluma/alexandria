from collections import Counter

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

from alexandria.core.models import Document, File
from alexandria.core.serializers import BaseSerializer
from alexandria.core.validation import BaseValidator, validator_for


def test_validation(db, reset_validators, document, file, admin_client):
    call_counter = Counter()

    class TestValidator(BaseValidator):
        @validator_for(Document)
        def validate(self, data):
            data["created_by_group"] = "foobar"
            call_counter["validate"] += 1
            # Ensure serializer is available and functional
            assert self.serializer
            assert self.serializer.context["request"].method == "PATCH"
            return data

    BaseSerializer.validation_classes = [TestValidator]

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


def test_validation_config_error(reset_validators):
    # We cannot have the same validator method for two models
    # (no chaining!)
    with pytest.raises(ImproperlyConfigured):

        class TestValidator(BaseValidator):
            @validator_for(Document)
            @validator_for(File)
            def validate(self, data):
                # needed for the decorator, but won't ever be called
                pass  # pragma: no cover

from django_filters import FilterSet, UUIDFilter

from . import models


class SignatureRequestFilterSet(FilterSet):
    document = UUIDFilter(field_name="file__document")

    class Meta:
        model = models.SignatureRequest
        fields = ["file", "document", "status", "signature_type"]


class SignatureFilterSet(FilterSet):
    class Meta:
        model = models.Signature
        fields = ["file", "signature_type", "signature_request"]

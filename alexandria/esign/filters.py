from django_filters import FilterSet

from . import models


class SignatureRequestFilterSet(FilterSet):
    class Meta:
        model = models.SignatureRequest
        fields = ["file", "status"]


class SignatureFilterSet(FilterSet):
    class Meta:
        model = models.Signature
        fields = ["file", "signature_type", "signature_request"]

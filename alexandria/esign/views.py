from django.db import IntegrityError, transaction
from django.utils.translation import gettext as _
from generic_permissions.permissions import PermissionViewMixin
from generic_permissions.visibilities import VisibilityViewMixin
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
)

from . import models, serializers
from .filters import SignatureFilterSet, SignatureRequestFilterSet


class SignatureRequestViewSet(
    PermissionViewMixin,
    VisibilityViewMixin,
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """Start (POST) and poll (GET) signature requests.

    Only one active request per file is allowed. If the requesting user
    already has an active request for the file, it is returned instead of
    creating a new one.
    """

    serializer_class = serializers.SignatureRequestSerializer
    queryset = models.SignatureRequest.objects.select_related("file")
    filterset_class = SignatureRequestFilterSet

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # The serializer rejects active requests of other users, so an active
        # request at this point belongs to the requesting user.
        active = (
            models.SignatureRequest.objects.active()
            .for_file(serializer.validated_data["file"])
            .first()
        )
        if active:
            return Response(self.get_serializer(active).data, status=HTTP_200_OK)

        try:
            with transaction.atomic():
                # TODO: prepare PDF, request signature at provider, handle
                # registration
                self.perform_create(serializer)
        except IntegrityError:
            # Concurrent request for the same file, caught by the unique
            # constraint on active requests
            raise ValidationError(
                _("A signature process for this file is already in progress.")
            )

        return Response(serializer.data, status=HTTP_201_CREATED)

    # TODO: retrieve: poll provider status while active and finish signing


class SignatureViewSet(
    PermissionViewMixin,
    VisibilityViewMixin,
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.SignatureSerializer
    queryset = models.Signature.objects.select_related("file", "signature_request")
    filterset_class = SignatureFilterSet

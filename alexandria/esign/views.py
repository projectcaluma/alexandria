from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from generic_permissions.visibilities import VisibilityViewMixin
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
)

from . import api, models, serializers, tasks
from .backends import get_backend
from .filters import SignatureFilterSet, SignatureRequestFilterSet


class SignatureRequestViewSet(
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

    The frontend does not know the backend. It starts a request, shows
    `action_url` (e.g. as QR code) if set, and polls until the request is no
    longer active.

    Only one active request per file is allowed. If the requesting user
    already has an active request for the file, it is returned instead of
    creating a new one.

    Write access is checked as `sign` object permission on the document (see
    `alexandria.esign.permissions`), not with permissions on this model.
    """

    # Signing needs a user and group, also with anonymous write enabled
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SignatureRequestSerializer
    queryset = models.SignatureRequest.objects.select_related(
        "file__document"
    ).prefetch_related("signatures__file", "file__document__files__signatures")
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
                signature_request = serializer.save()
                get_backend().request_signature(signature_request)
                signature_request.save()
                if signature_request.is_active:
                    tasks.cancel_expired_signature_request.apply_async_on_commit(
                        args=[signature_request.pk], eta=signature_request.timeout
                    )
        except IntegrityError:
            # Concurrent request for the same file, caught by the unique
            # constraint on active requests
            raise ValidationError(
                _("A signature process for this file is already in progress.")
            )

        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        signature_request = self.get_object()

        backend = get_backend()
        # Without backend (signing disabled afterwards) the state is kept
        if signature_request.is_active and backend:
            with transaction.atomic():
                # Lock, so concurrent polls don't finish the signature twice.
                # A poll already running holds the lock, skip instead of
                # waiting for its provider calls.
                locked = (
                    self.get_queryset()
                    .select_for_update(skip_locked=True, of=("self",))
                    .filter(pk=signature_request.pk)
                    .first()
                )
                if locked and locked.is_active:
                    self._poll(backend, locked)
                    signature_request = locked

        return Response(self.get_serializer(signature_request).data)

    def _poll(self, backend, signature_request):
        if not api.is_latest(signature_request.file):
            # Finishing would undo the changes of the newer version
            signature_request.status = models.SignatureRequest.Status.OUTDATED
            signature_request.prepared_content = None
        elif signature_request.timeout and signature_request.timeout <= timezone.now():
            api.end_expired_request(signature_request)
            return
        else:
            backend.poll_signature(signature_request)
        signature_request.save()


class SignatureViewSet(
    VisibilityViewMixin,
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """List signatures and stamp files (POST).

    Stamps need no confirmation, so they are created synchronously. Write
    access is checked as `stamp` object permission on the document.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SignatureSerializer
    queryset = models.Signature.objects.select_related("file", "signature_request")
    filterset_class = SignatureFilterSet

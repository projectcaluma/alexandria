import json

from django.conf import settings
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from generic_permissions.permissions import PermissionViewMixin
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

from alexandria.core.utils import get_user_and_group_from_request

from . import models, serializers, tasks
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

        # Without backend (signing disabled afterwards) the state is kept
        if signature_request.is_active and get_backend():
            with transaction.atomic():
                # Lock, so concurrent polls don't finish the signature twice
                signature_request = (
                    models.SignatureRequest.objects.select_for_update().get(
                        pk=signature_request.pk
                    )
                )
                if signature_request.is_active:
                    get_backend().poll_signature(signature_request)
                    signature_request.save()

        return Response(self.get_serializer(signature_request).data)


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


class DeepSignServiceAccountViewSet(
    PermissionViewMixin,
    VisibilityViewMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """Connection state of the DeepSign service account of the user's group.

    POST starts the connection and returns the DeepSign `connection_url`.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DeepSignServiceAccountSerializer
    queryset = models.DeepSignServiceAccount.objects.all()

    def get_queryset(self):
        # The connection URL contains the state token, only expose own group
        _user, group = get_user_and_group_from_request(self.request)
        return super().get_queryset().for_group(group)


@method_decorator(csrf_exempt, name="dispatch")
class DeepSignCallbackView(View):
    """Receive service account credentials from DeepSign.

    DeepSign makes the admin's browser post a form (`response_mode=form_post`)
    to this endpoint, so it is unauthenticated. The request is authenticated
    by the state token handed out with the connection URL.
    """

    http_method_names = ["post"]

    def post(self, request):
        try:
            state = json.loads(request.POST["state"])
            account = models.DeepSignServiceAccount.objects.get(
                group=state["group"], state_token=state["token"]
            )
            account.account_id = request.POST["service_account_id"]
            account.username = request.POST["service_account_username"]
            account.password = request.POST["service_account_password"]
        except (
            KeyError,
            TypeError,
            json.JSONDecodeError,
            models.DeepSignServiceAccount.DoesNotExist,
        ):
            return HttpResponseBadRequest()

        account.connected_at = timezone.now()
        # Invalidate the state, a callback can only be used once
        account.state_token = models.make_state_token()
        account.save()

        return HttpResponseRedirect(settings.ALEXANDRIA_DEEPSIGN_CALLBACK_REDIRECT_URL)

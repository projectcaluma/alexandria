from django.utils.translation import gettext as _
from rest_framework.exceptions import PermissionDenied
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import SerializerMethodResourceRelatedField

from alexandria.core.models import File
from alexandria.core.serializers import BaseSerializer
from alexandria.core.utils import get_user_and_group_from_request

from . import api, models
from .api import SIGNABLE_MIME_TYPES, stamp_file
from .backends import get_backend
from .permissions import SIGN, STAMP, has_document_permission


class SignableFileMixin:
    """Validate the `file` to sign and the group of the requesting user.

    `permission_action` is checked as object permission on the document.
    """

    permission_action = SIGN

    def validate_file(self, file):
        if file.variant != File.Variant.ORIGINAL:
            raise serializers.ValidationError(_("Only original files can be signed."))
        if file.mime_type not in SIGNABLE_MIME_TYPES:
            raise serializers.ValidationError(_("Only PDF files can be signed."))
        return file

    def validate(self, data):
        data = super().validate(data)
        _user, group = get_user_and_group_from_request(self.context.get("request"))

        backend = get_backend()
        if backend is None or not backend.is_enabled_for(group):
            raise serializers.ValidationError(
                _("Your organisation is not configured for signing.")
            )
        if not has_document_permission(
            self.context.get("request"), data["file"].document, self.permission_action
        ):
            raise PermissionDenied()
        # The backend signs with the account of `created_by_group`, which must
        # be the group checked above, not one passed by the client
        data["created_by_group"] = group
        return data


class SignatureRequestSerializer(SignableFileMixin, BaseSerializer):
    file = serializers.ResourceRelatedField(queryset=File.objects.all())
    is_current = serializers.SerializerMethodField()
    signer_name = serializers.SerializerMethodField()
    signed_file = SerializerMethodResourceRelatedField(model=File, read_only=True)

    included_serializers = {
        "file": "alexandria.core.serializers.FileSerializer",
    }

    def get_is_current(self, signature_request):
        """Whether the result is still part of the latest file.

        False once the document got a new version unrelated to signatures,
        see `api.current_files`.
        """
        document = signature_request.file.document
        # Shared by all requests of a list response
        cache = self.context.setdefault("esign_current_files", {})
        if document.pk not in cache:
            cache[document.pk] = {f.pk for f in api.current_files(document)}
        return signature_request.file_id in cache[document.pk]

    def _signature(self, signature_request):
        return next(iter(signature_request.signatures.all()), None)

    def get_signer_name(self, signature_request):
        """Name in the signing certificate, may differ from the user."""
        signature = self._signature(signature_request)
        return signature.signer_name if signature else None

    def get_signed_file(self, signature_request):
        """New version created by the signature, unset until done."""
        signature = self._signature(signature_request)
        return signature.file if signature else None

    def validate(self, data):
        data = super().validate(data)
        user, _group = get_user_and_group_from_request(self.context.get("request"))

        # An active request of the same user is resumed by the view
        if (
            models.SignatureRequest.objects.active()
            .for_file(data["file"])
            .exclude(created_by_user=user)
            .exists()
        ):
            raise serializers.ValidationError(
                _(
                    "A signature process for this file has already been "
                    "started by another user."
                )
            )

        return data

    class Meta:
        model = models.SignatureRequest
        fields = BaseSerializer.Meta.fields + (
            "file",
            "signature_type",
            "status",
            "timeout",
            "action_url",
            "provider_status",
            "is_current",
            "signer_name",
            "signed_file",
        )
        read_only_fields = (
            "signature_type",
            "status",
            "timeout",
            "action_url",
            "provider_status",
        )
        # The unique constraint on active requests is handled in the view:
        # an active request of the same user is returned instead of failing.
        validators = []


class SignatureSerializer(SignableFileMixin, BaseSerializer):
    """Signatures are created by signature requests, except stamps.

    Creating a signature stamps `file` (timestamp only, a visible stamp
    image can only be passed via `api.stamp_file`). The response contains
    the new signature, its `file` is the stamped new version.
    """

    permission_action = STAMP

    file = serializers.ResourceRelatedField(queryset=File.objects.all())
    signature_request = serializers.ResourceRelatedField(read_only=True)

    included_serializers = {
        "file": "alexandria.core.serializers.FileSerializer",
        "signature_request": SignatureRequestSerializer,
    }

    class Meta:
        model = models.Signature
        fields = BaseSerializer.Meta.fields + (
            "file",
            "signature_request",
            "signature_type",
            "signer_name",
            "signed_at",
            "signature_hash",
        )
        read_only_fields = tuple(field for field in fields if field != "file")

    def create(self, validated_data):
        user, _group = get_user_and_group_from_request(self.context.get("request"))
        return stamp_file(
            validated_data["file"],
            user=user,
            group=validated_data["created_by_group"],
        )



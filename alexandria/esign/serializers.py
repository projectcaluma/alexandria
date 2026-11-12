from django.utils.translation import gettext as _
from rest_framework_json_api import serializers

from alexandria.core.models import File
from alexandria.core.serializers import BaseSerializer
from alexandria.core.utils import get_user_and_group_from_request

from . import models

SIGNABLE_MIME_TYPES = ("application/pdf",)


class SignatureRequestSerializer(BaseSerializer):
    file = serializers.ResourceRelatedField(queryset=File.objects.all())

    included_serializers = {
        "file": "alexandria.core.serializers.FileSerializer",
    }

    def validate_file(self, file):
        if file.variant != File.Variant.ORIGINAL:
            raise serializers.ValidationError(_("Only original files can be signed."))
        if file.mime_type not in SIGNABLE_MIME_TYPES:
            raise serializers.ValidationError(_("Only PDF files can be signed."))
        return file

    def validate(self, data):
        data = super().validate(data)
        user, group = get_user_and_group_from_request(self.context.get("request"))

        if not models.SignatureProviderCredentials.objects.for_group(group).exists():
            raise serializers.ValidationError(
                _("Your organisation is not configured for signing.")
            )

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
            "status",
            "timeout",
        )
        read_only_fields = ("status", "timeout")
        # The unique constraint on active requests is handled in the view:
        # an active request of the same user is returned instead of failing.
        validators = []


class SignatureSerializer(BaseSerializer):
    file = serializers.ResourceRelatedField(read_only=True)
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
        read_only_fields = fields

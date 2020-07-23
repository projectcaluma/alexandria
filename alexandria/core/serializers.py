from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from . import models


class BaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        self.Meta.model.check_permissions(self.context["request"])
        if self.instance is not None:
            self.instance.check_object_permissions(self.context["request"])

        user = self.context["request"].user
        group = user.group if not isinstance(user, AnonymousUser) else None

        validated_data["modified_by_user"] = user.username
        validated_data["modified_by_group"] = group
        if self.instance is not None:
            validated_data["created_by_user"] = user.username
            validated_data["created_by_group"] = group
        return validated_data

    class Meta:
        fields = (
            "created_at",
            "created_by_user",
            "created_by_group",
            "modified_at",
            "modified_by_user",
            "modified_by_group",
            "meta",
        )


class CategorySerializer(BaseSerializer):
    class Meta:
        model = models.Category
        fields = BaseSerializer.Meta.fields + ("name", "description", "color")


class TagSerializer(BaseSerializer):
    class Meta:
        model = models.Tag
        fields = BaseSerializer.Meta.fields + ("name", "description")


class FileSerializer(BaseSerializer):
    renderings = serializers.ResourceRelatedField(
        required=False, many=True, read_only=True,
    )

    included_serializers = {
        "document": "alexandria.core.serializers.DocumentSerializer",
        "original": "alexandria.core.serializers.FileSerializer",
        "renderings": "alexandria.core.serializers.FileSerializer",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We only want to provide an upload_url on creation of a file.
        self.new = False
        if "request" in self.context and self.context["request"].method == "POST":
            self.new = True

    download_url = serializers.CharField(read_only=True)
    upload_url = serializers.SerializerMethodField()

    def get_upload_url(self, obj):
        return obj.upload_url if self.new else ""

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        if validated_data.get(
            "type"
        ) != models.File.ORIGINAL and not validated_data.get("original"):
            f_type = validated_data.get("type")
            raise ValidationError(f'"original" must be set for type "{f_type}".')

        if validated_data.get("type") == models.File.ORIGINAL and validated_data.get(
            "original"
        ):
            f_type = validated_data.get("type")
            raise ValidationError(f'"original" must not be set for type "{f_type}".')

        return validated_data

    class Meta:
        model = models.File
        fields = BaseSerializer.Meta.fields + (
            "type",
            "name",
            "original",
            "renderings",
            "document",
            "download_url",
            "upload_url",
        )


class DocumentSerializer(BaseSerializer):
    files = serializers.ResourceRelatedField(
        queryset=models.File.objects.all(), required=False, many=True
    )
    included_serializers = {
        "category": CategorySerializer,
        "tags": TagSerializer,
        "files": FileSerializer,
    }

    class Meta:
        model = models.Document
        fields = BaseSerializer.Meta.fields + (
            "files",
            "title",
            "description",
            "category",
            "tags",
        )

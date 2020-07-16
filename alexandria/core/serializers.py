from django.contrib.auth.models import AnonymousUser
from rest_framework_json_api import serializers

from . import models


class BaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

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
        fields = BaseSerializer.Meta.fields + ("name", "description")


class TagSerializer(BaseSerializer):
    class Meta:
        model = models.Tag
        fields = BaseSerializer.Meta.fields + ("name", "description")


class FileSerializer(BaseSerializer):
    included_serializers = {
        "document": "alexandria.core.serializers.DocumentSerializer",
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

    class Meta:
        model = models.File
        fields = BaseSerializer.Meta.fields + (
            "name",
            "document",
            "download_url",
            "upload_url",
        )


class DocumentSerializer(BaseSerializer):
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

from rest_framework_json_api import serializers

from . import models


class BaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)
        user = self.context["request"].user
        validated_data["modified_by_user"] = user.username
        validated_data["modified_by_group"] = user.group
        if self.instance is not None:
            validated_data["created_by_user"] = user.username
            validated_data["created_by_group"] = user.group
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


class DocumentSerializer(BaseSerializer):
    included_serializers = {
        "category": CategorySerializer,
        "tags": TagSerializer,
    }

    class Meta:
        model = models.Document
        fields = BaseSerializer.Meta.fields + (
            "name",
            "title",
            "description",
            "category",
            "tags",
        )

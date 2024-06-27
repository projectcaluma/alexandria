import json
import logging

from django.conf import settings
from django.db.transaction import atomic
from django.template.defaultfilters import slugify
from django.utils import translation
from django.utils.module_loading import import_string
from generic_permissions.validation import ValidatorMixin
from generic_permissions.visibilities import (
    VisibilityResourceRelatedField,
    VisibilitySerializerMixin,
)
from rest_framework_json_api import serializers

from . import models

log = logging.getLogger(__name__)


class BaseSerializer(
    ValidatorMixin, VisibilitySerializerMixin, serializers.ModelSerializer
):
    serializer_related_field = VisibilityResourceRelatedField

    created_at = serializers.DateTimeField(read_only=True)

    def get_user_and_group(self):
        return import_string(settings.ALEXANDRIA_GET_USER_AND_GROUP_FUNCTION)(
            self.context.get("request")
        )

    def is_valid(self, *args, **kwargs):
        # Prime data so the validators are called (and default values filled
        # if client didn't pass them.)
        user, group = self.get_user_and_group()
        self.initial_data.setdefault("created_by_group", group)
        self.initial_data.setdefault("modified_by_group", group)
        self.initial_data.setdefault("created_by_user", user)
        self.initial_data.setdefault("modified_by_user", user)
        return super().is_valid(*args, **kwargs)

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        user, group = self.get_user_and_group()
        validated_data["modified_by_user"] = user
        validated_data["modified_by_group"] = group

        return validated_data

    def validate_created_by_user(self, value):
        # Created by user can be set on creation, then must remain constant
        if self.instance:
            # can't change created_by_user on existing instances
            return self.instance.created_by_user
        return value

    def validate_created_by_group(self, value):
        # Created by group can be set on creation, then must remain constant
        if self.instance:
            # can't change created_by_group on existing instances
            return self.instance.created_by_group
        return value

    class Meta:
        fields = (
            "created_at",
            "created_by_user",
            "created_by_group",
            "modified_at",
            "modified_by_user",
            "modified_by_group",
            "metainfo",
        )


class SlugModelSerializer(BaseSerializer):
    """
    Ensure on creation that the model will receive a slug.

    If no slug is passed via API, one is derived from the `name` field of
    the model, via Django's `slugify()` helper. If the model in question
    does not have a `name` field, you can specify a `slug_source_field`
    attribute on your serializer's `Meta` class to tell it which
    field to use instead.
    """

    def create(self, validated_data):
        slug_field = getattr(self.Meta, "slug_source_field", "name")
        if "slug" not in validated_data:
            slug_source_value = validated_data.get(slug_field)
            if isinstance(slug_source_value, dict):  # pragma: todo cover
                lang = translation.get_language()
                slug_source_value = slug_source_value.get(lang)
            validated_data["slug"] = slugify(slug_source_value)

        return super().create(validated_data)


class CategorySerializer(SlugModelSerializer):
    parent = serializers.ResourceRelatedField(required=False, read_only=True)
    children = serializers.ResourceRelatedField(
        required=False, read_only=True, many=True
    )

    included_serializers = {
        "parent": "alexandria.core.serializers.CategorySerializer",
        "children": "alexandria.core.serializers.CategorySerializer",
    }

    class Meta:
        model = models.Category
        fields = SlugModelSerializer.Meta.fields + (
            "name",
            "description",
            "allowed_mime_types",
            "color",
            "parent",
            "children",
        )


class TagSynonymGroupSerializer(BaseSerializer):
    tags = serializers.ResourceRelatedField(required=False, read_only=True, many=True)

    class Meta:
        model = models.TagSynonymGroup
        fields = BaseSerializer.Meta.fields + ("tags",)


class TagSerializer(BaseSerializer):
    included_serializers = {
        "tag_synonym_group": "alexandria.core.serializers.TagSynonymGroupSerializer"
    }

    class Meta:
        model = models.Tag
        fields = BaseSerializer.Meta.fields + (
            "name",
            "description",
            "tag_synonym_group",
        )


class MarkSerializer(SlugModelSerializer):
    class Meta:
        model = models.Mark
        fields = SlugModelSerializer.Meta.fields + (
            "name",
            "description",
        )
        slug_source_field = "name"


class FileSerializer(BaseSerializer):
    renderings = serializers.ResourceRelatedField(
        required=False,
        many=True,
        read_only=True,
    )

    included_serializers = {
        "document": "alexandria.core.serializers.DocumentSerializer",
        "original": "alexandria.core.serializers.FileSerializer",
        "renderings": "alexandria.core.serializers.FileSerializer",
    }

    download_url = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We only want to provide an upload_url on creation of a file.
        self.new = False
        if "request" in self.context and self.context["request"].method == "POST":
            self.new = True

    def get_download_url(self, instance):
        return instance.get_download_url(self.context.get("request"))

    def validate(self, *args, **kwargs):
        """Validate the data.

        Validation can be extended by adding ValidatorClass to the
        `validator_classes` attribute of the FileViewSet.
        """
        validated_data = super().validate(*args, **kwargs)

        # TODO: When next working on file / storage stuff, consider extracting
        # the storage code into it's own project, so we can reuse it outside
        # of Alexandria: https://github.com/projectcaluma/alexandria/issues/480
        if settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION:
            validated_data["encryption_status"] = settings.ALEXANDRIA_ENCRYPTION_METHOD

        validated_data["size"] = validated_data["content"].size

        return validated_data

    def _prepare_multipart(self):
        """Massage multipart data into jsonapi-compatible form."""

        # Depending on incoming data, the parser converts the request into
        # a dict or an immutable QueryDict. In the latter case, we cannot
        # modify the dict anymore to accomodate the multipart -> jsonapi
        # conversion as needed, thus we need to unlock it.
        # As nothing bad comes from just leaving it "mutable", we don't
        # bother cleaning it up after.
        if hasattr(self.initial_data, "_mutable"):
            self.initial_data._mutable = True

        if not isinstance(self.initial_data.get("document"), dict):
            self.initial_data["document"] = {
                "type": "documents",
                "id": self.initial_data["document"],
            }

    def is_valid(self, *args, raise_exception=False, **kwargs):
        # TODO: When next working on file / storage stuff, consider extracting
        # the storage code into it's own project, so we can reuse it outside
        # of Alexandria: https://github.com/projectcaluma/alexandria/issues/480

        if self.context["request"].content_type.startswith("multipart/"):
            self._prepare_multipart()
        return super().is_valid(*args, raise_exception=raise_exception, **kwargs)

    class Meta:
        model = models.File
        fields = BaseSerializer.Meta.fields + (
            "variant",
            "name",
            "original",
            "renderings",
            "document",
            "checksum",
            "content",
            "download_url",
            "mime_type",
            "size",
        )
        read_only_fields = (
            "variant",
            "original",
            "mime_type",
            "size",
        )
        extra_kwargs = {"content": {"write_only": True}}


class DocumentSerializer(BaseSerializer):
    category = serializers.ResourceRelatedField(queryset=models.Category.objects)
    files = serializers.ResourceRelatedField(
        queryset=models.File.objects.all(), required=False, many=True
    )
    content = serializers.FileField(write_only=True, required=True)

    included_serializers = {
        "category": CategorySerializer,
        "tags": TagSerializer,
        "marks": MarkSerializer,
        "files": FileSerializer,
    }

    @atomic
    def create(self, validated_data):
        content = validated_data.pop("content")
        document = super().create(validated_data)

        file_data = {
            "name": content.name,
            "document": {
                "type": "documents",
                "id": document.pk,
            },
            "content": content,
        }
        file_serializer = FileSerializer(data=file_data, context=self.context)
        file_serializer.is_valid(raise_exception=True)
        file_serializer.save()

        return document

    def _prepare_multipart(self):
        """Massage multipart data into jsonapi-compatible form."""
        self.initial_data = self.initial_data.dict()

        self.initial_data["data"].seek(0)
        self.initial_data.update(
            json.loads(self.initial_data["data"].read().decode("utf-8"))
        )
        if not isinstance(self.initial_data.get("category"), dict):
            self.initial_data["category"] = {
                "type": "categories",
                "id": self.initial_data["category"],
            }

    def is_valid(self, *args, raise_exception=False, **kwargs):
        if self.context["request"].content_type.startswith("multipart/"):
            self._prepare_multipart()
        return super().is_valid(*args, raise_exception=raise_exception, **kwargs)

    class Meta:
        model = models.Document
        fields = BaseSerializer.Meta.fields + (
            "files",
            "title",
            "description",
            "date",
            "category",
            "tags",
            "marks",
            "content",
        )
        extra_kwargs = {"content": {"write_only": True}}


class WebDAVSerializer(BaseSerializer):
    webdav_url = serializers.SerializerMethodField()

    def get_webdav_url(self, instance):
        request = self.context.get("request")
        host = request.get_host() if request else "localhost"
        scheme = request.scheme if request else "http"
        user, group = self.get_user_and_group()
        return instance.get_latest_original().get_webdav_url(
            user, group, f"{scheme}://{host}"
        )

    class Meta:
        model = models.Document
        fields = ("webdav_url",)

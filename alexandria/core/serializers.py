from typing import Optional, Tuple

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.template.defaultfilters import slugify
from django.utils import timezone, translation
from django.utils.http import urlsafe_base64_encode
from generic_permissions.validation import ValidatorMixin
from preview_generator.manager import hashlib
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import reverse

from . import models


class BaseSerializer(ValidatorMixin, serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    def is_valid(self, *args, **kwargs):
        # Prime data so the validators are called (and default values filled
        # if client didn't pass them.)
        self.initial_data.setdefault("created_by_group", self._default_group())
        self.initial_data.setdefault("modified_by_group", self._default_group())
        return super().is_valid(*args, **kwargs)

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        user = self.context["request"].user
        username = getattr(user, settings.ALEXANDRIA_CREATED_BY_USER_PROPERTY)
        validated_data["created_by_user"] = username
        validated_data["modified_by_user"] = username

        return validated_data

    def validate_created_by_group(self, value):
        # Created by group can be set on creation, then must remain constant
        if self.instance:
            # can't change created_by_group on existing instances
            return self.instance.created_by_group
        return value

    def _default_group(self):
        user = self.context["request"].user
        return (
            getattr(user, settings.ALEXANDRIA_CREATED_BY_GROUP_PROPERTY)
            if not isinstance(user, AnonymousUser)
            else None
        )

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
            "color",
            "parent",
            "children",
        )


class TagSynonymGroupSerializer(BaseSerializer):
    tags = serializers.ResourceRelatedField(required=False, read_only=True, many=True)

    class Meta:
        model = models.TagSynonymGroup
        fields = BaseSerializer.Meta.fields + ("tags",)


class TagSerializer(SlugModelSerializer):
    included_serializers = {
        "tag_synonym_group": "alexandria.core.serializers.TagSynonymGroupSerializer"
    }

    class Meta:
        model = models.Tag
        fields = SlugModelSerializer.Meta.fields + (
            "name",
            "description",
            "tag_synonym_group",
        )
        slug_source_field = "name"


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

    @staticmethod
    def make_signature_components(
        pk: str, request: Request, expires: Optional[int] = None
    ) -> Tuple[str, int, str]:
        """Make the components used to sign and verify the download_url.

        If `expires` is provided the components are called for the verification step.

        Otherwise expiry is calculated and returned
        """
        if not expires:
            expires = int(
                (
                    timezone.now()
                    + timezone.timedelta(
                        seconds=settings.ALEXANDRIA_DOWNLOAD_URL_LIFETIME
                    )
                ).timestamp()
            )
        download_path = reverse("file-download", args=[pk])
        host = f"{request.META.get('wsgi.url_scheme', 'http')}://{request.get_host()}"
        url = f"{host.strip('/')}{download_path}"
        token = f"{url}{expires}{settings.SECRET_KEY}"
        hash = hashlib.shake_256(token.encode())
        # Django's base64 encoder strips padding and ascii-decodes the output
        signature = urlsafe_base64_encode(hash.digest(32))
        return url, expires, signature

    def get_download_url(self, instance):
        request = self.context.get("request")
        if not request:
            return None
        url, expires, signature = self.make_signature_components(
            str(instance.pk), request
        )
        return f"{url}?expires={expires}&signature={signature}"

    def validate(self, *args, **kwargs):
        """Validate the data.

        Validation can be extended by adding ValidatorClass to the
        `validator_classes` attribute of the FileViewSet.
        """
        validated_data = super().validate(*args, **kwargs)
        if validated_data.get(
            "variant"
        ) != models.File.Variant.ORIGINAL and not validated_data.get("original"):
            file_variant = validated_data.get("variant")
            raise ValidationError(
                f'"original" must be set for variant "{file_variant}".'
            )

        if (
            variant := validated_data.get("variant")
        ) == models.File.Variant.ORIGINAL and validated_data.get("original"):
            raise ValidationError(
                f'"original" must not be set for variant "{variant}".'
            )

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

        if (original := self.initial_data.get("original")) and not isinstance(
            original, dict
        ):
            self.initial_data["original"] = {"type": "files", "id": original}

    def is_valid(self, *args, raise_exception=False, **kwargs):
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
        )
        extra_kwargs = {"content": {"write_only": True}}


class DocumentSerializer(BaseSerializer):
    files = serializers.ResourceRelatedField(
        queryset=models.File.objects.all(), required=False, many=True
    )
    included_serializers = {
        "category": CategorySerializer,
        "tags": TagSerializer,
        "marks": MarkSerializer,
        "files": FileSerializer,
    }

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
        )

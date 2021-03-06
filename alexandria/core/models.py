import re
import uuid

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import LocalizedCharField, LocalizedTextField
from rest_framework import exceptions

from .storage_clients import client


def make_uuid():
    """Return a new random UUID value.

    This indirection is done for testing purposes, so test code can mock
    uuid.uuid4(). If we wouldn't do this, then the models would have a direct
    reference that doesn't get mocked away.

    We can't replace it with a lambda because Django Migrations can't handle them.
    """
    return uuid.uuid4()


class VisibilityMixin:
    visibility_classes = None

    @classmethod
    def visibility_queryset_filter(cls, queryset, request, **kwargs):
        if cls.visibility_classes is None:
            raise ImproperlyConfigured(
                "check that app `alexandria.core.apps.DefaultConfig` is part of your `INSTALLED_APPS`."
            )

        for visibility_class in cls.visibility_classes:
            queryset = visibility_class().filter_queryset(cls, queryset, request)

        return queryset


class PermissionMixin:
    permission_classes = None

    @classmethod
    def check_permissions(cls, request, **kwargs):
        if cls.permission_classes is None:
            raise ImproperlyConfigured(
                "check that app `alexandria.core.apps.DefaultConfig` is part of your `INSTALLED_APPS`."
            )

        for permission_class in cls.permission_classes:
            if not permission_class().has_permission(cls, request):
                raise exceptions.PermissionDenied()

    def check_object_permissions(self, request):
        for permission_class in self.permission_classes:
            if not permission_class().has_object_permission(
                self.__class__, request, self
            ):
                raise exceptions.PermissionDenied()


class BaseModel(PermissionMixin, VisibilityMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by_user = models.CharField(
        _("created by user"), max_length=150, blank=True, null=True
    )
    created_by_group = models.CharField(
        _("created by group"), max_length=255, blank=True, null=True
    )
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    modified_by_user = models.CharField(
        _("created by user"), max_length=150, blank=True, null=True
    )
    modified_by_group = models.CharField(
        _("created by group"), max_length=255, blank=True, null=True
    )
    meta = JSONField(_("meta"), default=dict)

    class Meta:
        abstract = True


class UUIDModel(BaseModel):
    """
    Models which use uuid as primary key.

    Defined as alexandria default
    """

    id = models.UUIDField(primary_key=True, default=make_uuid, editable=False)

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    """
    Models which use a slug as primary key.

    Defined as alexandria default for configuration so it is possible
    to merge between developer and user configuration.
    """

    slug = models.SlugField(max_length=255, primary_key=True)

    class Meta:
        abstract = True


COLOR_RE = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
color_validator = RegexValidator(COLOR_RE, _("Enter a valid color."), "invalid")


class Category(SlugModel):
    name = LocalizedCharField(
        _("category name"), blank=False, null=False, required=False
    )
    description = LocalizedTextField(
        _("category description"), null=True, blank=True, required=False
    )
    color = models.CharField(
        max_length=18, default="#FFFFFF", validators=[color_validator],
    )


class Tag(SlugModel):
    name = models.CharField(_("tag name"), blank=False, null=False, max_length=100)
    description = LocalizedTextField(
        _("tag description"), null=True, blank=True, required=False
    )


class Document(UUIDModel):
    title = LocalizedCharField(
        _("document title"), blank=True, null=True, required=False
    )
    description = LocalizedTextField(
        _("document description"), null=True, blank=True, required=False
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="documents")


class File(UUIDModel):
    ORIGINAL = "original"
    THUMBNAIL = "thumbnail"

    TYPE_CHOICES = (
        ORIGINAL,
        THUMBNAIL,
    )
    TYPE_CHOICES_TUPLE = ((type_choice, type_choice) for type_choice in TYPE_CHOICES)
    type = models.CharField(choices=TYPE_CHOICES_TUPLE, max_length=23, default=ORIGINAL)
    original = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="renderings",
    )
    name = models.CharField(_("file name"), max_length=255)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="files"
    )

    class Meta:
        ordering = ["-created_at"]

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        client.remove_object(self.object_name)

    @property
    def object_name(self):
        return f"{self.pk}_{self.name}"

    @property
    def upload_url(self):
        return client.upload_url(self.object_name)

    @property
    def download_url(self):
        return client.download_url(self.object_name)

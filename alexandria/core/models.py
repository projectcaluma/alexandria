import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import LocalizedCharField, LocalizedTextField


def make_uuid():
    """Return a new random UUID value.

    This indirection is done for testing purposes, so test code can mock
    uuid.uuid4(). If we wouldn't do this, then the models would have a direct
    reference that doesn't get mocked away.

    We can't replace it with a lambda because Django Migrations can't handle them.
    """
    return uuid.uuid4()


class BaseModel(models.Model):
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


class Category(SlugModel):
    name = LocalizedCharField(
        _("category name"), blank=False, null=False, required=False
    )
    description = LocalizedTextField(
        _("category description"), null=True, blank=True, required=False
    )


class Tag(SlugModel):
    name = LocalizedCharField(_("tag name"), blank=False, null=False, required=False)
    description = LocalizedTextField(
        _("tag description"), null=True, blank=True, required=False
    )


class Document(UUIDModel):
    name = models.CharField(_("document name"), max_length=255)
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

import re
import uuid
from pathlib import Path

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_presigned_url.presign_urls import make_presigned_url
from localized_fields.fields import LocalizedCharField, LocalizedTextField
from manabi.token import Key, Token
from rest_framework_json_api.relations import reverse

from alexandria.storages.fields import DynamicStorageFileField


def upload_file_content_to(instance, _):
    return f"{instance.pk}_{instance.name}"


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
        _("Created by user"), max_length=150, blank=True, null=True
    )
    created_by_group = models.CharField(
        _("Created by group"), max_length=255, blank=True, null=True
    )
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    modified_by_user = models.CharField(
        _("Modified by user"), max_length=150, blank=True, null=True
    )
    modified_by_group = models.CharField(
        _("Modified by group"), max_length=255, blank=True, null=True
    )
    metainfo = models.JSONField(_("Metainfo"), default=dict)

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
color_validator = RegexValidator(
    COLOR_RE, _("Please enter a valid HEX color code."), "invalid"
)


class Category(SlugModel):
    name = LocalizedCharField(_("Name"), blank=False, null=False, required=False)
    description = LocalizedTextField(
        _("Description"), null=True, blank=True, required=False
    )
    allowed_mime_types = ArrayField(
        base_field=models.CharField(max_length=255),
        blank=True,
        null=True,
        verbose_name=_("Allowed mime types"),
    )
    color = models.CharField(
        max_length=18,
        default="#FFFFFF",
        validators=[color_validator],
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )
    sort = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ("sort",)


class TagSynonymGroup(BaseModel):
    pass


class Tag(UUIDModel):
    name = models.CharField(_("Name"), blank=False, null=False, max_length=100)
    description = LocalizedTextField(
        _("Description"), null=True, blank=True, required=False
    )
    tag_synonym_group = models.ForeignKey(
        TagSynonymGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="tags",
    )


class Mark(SlugModel):
    name = LocalizedCharField(_("Name"), blank=False, null=False, required=False)
    description = LocalizedTextField(
        _("Description"), null=True, blank=True, required=False
    )


class Document(UUIDModel):
    title = models.CharField(_("Title"), blank=True, null=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="documents")
    marks = models.ManyToManyField(Mark, blank=True, related_name="documents")
    date = models.DateField(blank=True, null=True)

    def get_latest_original(self) -> "File":
        if not self.files.count():
            raise ObjectDoesNotExist("Document has no files")
        return self.files.filter(variant=File.Variant.ORIGINAL).latest("created_at")

    @transaction.atomic()
    def clone(self):
        latest_original = self.get_latest_original()

        self.pk = None
        self.save()
        new_name = f"{self.pk}_{latest_original.name}"

        latest_original.pk = None
        latest_original.document = self
        latest_original.content.copy(new_name)

        return self


class File(UUIDModel):
    class EncryptionStatus(models.TextChoices):
        NOT_ENCRYPTED = "none", "No at-rest enryption"
        SSEC_GLOBAL_KEY = "ssec-global", "SSE-C global key encryption (AES256)"
        # NOTE: per object encryption is not implemented yet
        SSEC_OBJECT_KEY = "ssec-object", "SSE-C per object encryption (AES256)"

        __empty__ = "Encryption status not set"

    class Variant(models.TextChoices):
        ORIGINAL = "original", "original"
        THUMBNAIL = "thumbnail", "thumbnail"

    variant = models.CharField(
        choices=Variant.choices, max_length=23, default=Variant.ORIGINAL
    )
    original = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="renderings",
    )
    name = models.CharField(_("Name"), max_length=255)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="files"
    )
    checksum = models.CharField(_("Checksum"), max_length=255, null=True, blank=True)
    encryption_status = models.CharField(
        choices=EncryptionStatus.choices,
        max_length=12,
        default=None,
        null=True,
        blank=True,
    )

    content_vector = SearchVectorField(null=True, blank=True)
    content_text = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, blank=True, null=True)

    # TODO: When next working on file / storage stuff, consider extracting
    # the storage code into it's own project, so we can reuse it outside
    # of Alexandria: https://github.com/projectcaluma/alexandria/issues/480
    content = DynamicStorageFileField(upload_to=upload_file_content_to, max_length=300)
    mime_type = models.CharField(max_length=255)
    size = models.IntegerField()

    def get_webdav_url(self, username, group, host="http://localhost:8000"):
        # The path used to lock the file consists of the UUID and the actual
        # filename in order to be able to identify the correct file but also
        # show a meaningful filename in the respective editor (e.g. MS Word).
        path = Path(str(self.pk)) / Path(self.name)

        key = Key.from_dictionary({"manabi": {"key": settings.MANABI_SHARED_KEY}})

        # We encode `username` and `group` into the token to easily
        # apply/validate `user` and `group`
        payload = (username, group)
        token = Token(key, path, payload=payload)

        try:
            handler = settings.ALEXANDRIA_MANABI_DAV_URI_SCHEMES[self.mime_type]
        except KeyError:
            raise ImproperlyConfigured(
                f'The MIME type "{self.mime_type}" is configured in'
                "`ALEXANDRIA_MANABI_ALLOWED_MIMETYPES` but has no URI scheme"
                "configured. Please add the associated URI scheme in"
                "`ALEXANDRIA_MANABI_DAV_URI_SCHEMES`"
            )

        return (
            f"{handler}{host}{settings.ALEXANDRIA_MANABI_DAV_URL_PATH}/{token.as_url()}"
        )

    def get_download_url(self, request):
        if not request:
            return None

        return make_presigned_url(reverse("file-download", args=[self.pk]), request)

    class Meta:
        ordering = ["-created_at"]
        indexes = [GinIndex(fields=["content_vector"])]


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete file from filesystem when `File` object is deleted."""

    instance.content.delete(save=False)


@receiver(models.signals.post_save, sender=File)
def set_file_attributes(sender, instance, **kwargs):
    from alexandria.core import tasks

    if settings.ALEXANDRIA_ENABLE_CHECKSUM and not instance.checksum:
        tasks.set_checksum.delay_on_commit(instance.pk)

    if (
        settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH
        and instance.variant == File.Variant.ORIGINAL
        and not instance.content_vector
    ):
        tasks.set_content_vector.delay_on_commit(instance.pk)

    if (
        instance.variant == File.Variant.ORIGINAL
        and instance.renderings.count() < 1
        and settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION
    ):
        tasks.create_thumbnail.delay_on_commit(instance.pk)

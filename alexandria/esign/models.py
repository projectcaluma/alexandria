from django.db import models
from django.utils.translation import gettext_lazy as _

from alexandria.core.models import File, UUIDModel


class SignatureProviderCredentialsQuerySet(models.QuerySet):
    def for_group(self, group):
        return self.filter(group=group)


class SignatureProviderCredentials(UUIDModel):
    """Service account of a signature provider, one per group (organisation).

    Only groups with credentials are allowed to request signatures.
    """

    class Provider(models.TextChoices):
        DEEPSIGN = "deepsign", "DeepSign"

    group = models.CharField(_("Group"), max_length=255, unique=True)
    provider = models.CharField(
        _("Provider"),
        max_length=32,
        choices=Provider.choices,
        default=Provider.DEEPSIGN,
    )
    account_id = models.CharField(_("Account ID"), max_length=255)
    username = models.CharField(_("Username"), max_length=255)
    # TODO: encrypt at rest
    password = models.CharField(_("Password"), max_length=255)

    objects = SignatureProviderCredentialsQuerySet.as_manager()

    class Meta:
        verbose_name = _("Signature provider credentials")
        verbose_name_plural = _("Signature provider credentials")

    def __str__(self):
        return f"{self.group} ({self.get_provider_display()})"


class SignatureRequestStatus(models.TextChoices):
    OPEN = "open", _("Open")
    REQUESTED = "requested", _("Requested")
    CONFIRMED = "confirmed", _("Confirmed")
    DONE = "done", _("Done")
    TIMEOUT = "timeout", _("Timeout")
    REJECTED = "rejected", _("Rejected")


ACTIVE_SIGNATURE_REQUEST_STATUSES = (
    SignatureRequestStatus.OPEN,
    SignatureRequestStatus.REQUESTED,
    SignatureRequestStatus.CONFIRMED,
)


class SignatureRequestQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=ACTIVE_SIGNATURE_REQUEST_STATUSES)

    def for_file(self, file):
        return self.filter(file=file)


class SignatureRequest(UUIDModel):
    """State of an asynchronous signature request between polls.

    The requesting user is stored in `created_by_user`.
    """

    Status = SignatureRequestStatus

    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        related_name="signature_requests",
        help_text=_("File to be signed"),
    )
    status = models.CharField(
        _("Status"),
        max_length=16,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True,
    )
    hash_key = models.CharField(
        _("Hash key"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("ID of the signature request at the provider"),
    )
    timeout = models.DateTimeField(
        _("Timeout"),
        null=True,
        blank=True,
        help_text=_("After this point in time the request is cleaned up"),
    )
    digest = models.JSONField(
        _("Digest"),
        null=True,
        blank=True,
        help_text=_("Serialized prepared byte range digest"),
    )
    prepared_content = models.BinaryField(
        _("Prepared content"),
        null=True,
        blank=True,
        help_text=_("PDF with reserved signature space, kept between polls"),
    )

    objects = SignatureRequestQuerySet.as_manager()

    class Meta:
        verbose_name = _("Signature request")
        verbose_name_plural = _("Signature requests")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["file"],
                condition=models.Q(status__in=ACTIVE_SIGNATURE_REQUEST_STATUSES),
                name="unique_active_signature_request_per_file",
                violation_error_message=_(
                    "A signature process for this file is already in progress."
                ),
            )
        ]

    def __str__(self):
        return f"{self.file_id} ({self.status})"

    @property
    def is_active(self):
        return self.status in ACTIVE_SIGNATURE_REQUEST_STATUSES


class Signature(UUIDModel):
    """Metadata of a signature embedded in a file."""

    class Type(models.TextChoices):
        TIMESTAMP = "timestamp", _("Timestamp")
        ADVANCED = "advanced", _("Advanced")
        QUALIFIED = "qualified", _("Qualified")

    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        related_name="signatures",
        help_text=_("File containing the signature"),
    )
    signature_request = models.ForeignKey(
        SignatureRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="signatures",
    )
    signature_type = models.CharField(
        _("Signature type"), max_length=16, choices=Type.choices
    )
    signer_name = models.CharField(
        _("Signer name"),
        max_length=255,
        blank=True,
        help_text=_("Name read from the signature certificate"),
    )
    signed_at = models.DateTimeField(_("Signed at"))
    signature_hash = models.CharField(_("Signature hash"), max_length=255)

    class Meta:
        verbose_name = _("Signature")
        verbose_name_plural = _("Signatures")
        ordering = ["-signed_at"]

    def __str__(self):
        return (
            f"{self.get_signature_type_display()} {self.signer_name} ({self.signed_at})"
        )

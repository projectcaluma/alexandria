from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from alexandria.esign import tasks
from alexandria.esign.models import SignatureRequest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "status,timeout_delta,expected_status",
    [
        (
            SignatureRequest.Status.REQUESTED,
            timedelta(minutes=-1),
            SignatureRequest.Status.TIMEOUT,
        ),
        (
            SignatureRequest.Status.REQUESTED,
            timedelta(minutes=1),
            SignatureRequest.Status.REQUESTED,
        ),
        (
            SignatureRequest.Status.DONE,
            timedelta(minutes=-1),
            SignatureRequest.Status.DONE,
        ),
    ],
)
def test_cancel_expired_signature_request(
    signature_request_factory, status, timeout_delta, expected_status
):
    signature_request = signature_request_factory(
        status=status, timeout=timezone.now() + timeout_delta
    )

    tasks.cancel_expired_signature_request(str(signature_request.pk))

    signature_request.refresh_from_db()
    assert signature_request.status == expected_status


@pytest.mark.django_db
def test_cancel_deleted_signature_request(signature_request_factory):
    signature_request = signature_request_factory()
    pk = str(signature_request.pk)
    signature_request.delete()

    tasks.cancel_expired_signature_request(pk)


@pytest.mark.django_db
def test_create_schedules_cleanup(mocker, admin_client, file_factory):
    schedule = mocker.patch.object(
        tasks.cancel_expired_signature_request, "apply_async_on_commit"
    )
    file = file_factory(mime_type="application/pdf")

    admin_client.post(
        reverse("signaturerequest-list"),
        {
            "data": {
                "type": "signature-requests",
                "relationships": {
                    "file": {"data": {"type": "files", "id": str(file.pk)}}
                },
            }
        },
    )

    signature_request = SignatureRequest.objects.get()
    schedule.assert_called_once_with(
        args=[signature_request.pk], eta=signature_request.timeout
    )


@pytest.mark.django_db
def test_cancel_signing_disabled(settings, signature_request_factory):
    signature_request = signature_request_factory(
        status=SignatureRequest.Status.REQUESTED,
        timeout=timezone.now() - timedelta(minutes=1),
    )
    settings.ALEXANDRIA_ESIGN_BACKEND = None

    tasks.cancel_expired_signature_request(str(signature_request.pk))

    signature_request.refresh_from_db()
    assert signature_request.status == SignatureRequest.Status.REQUESTED

from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone

from alexandria.esign.backends import get_backend
from alexandria.esign.models import SignatureRequest
from celery import shared_task

logger = get_task_logger(__name__)


@shared_task
def cancel_expired_signature_request(signature_request_pk: str):
    """Clean up a request the frontend stopped polling.

    Scheduled for the timeout of the request. Fetches the final state once
    more (the user may have confirmed in the meantime), otherwise ends the
    request and drops the prepared PDF.
    """
    with transaction.atomic():
        signature_request = (
            SignatureRequest.objects.select_for_update()
            .filter(pk=signature_request_pk)
            .first()
        )
        if (
            signature_request is None
            or not signature_request.is_active
            or signature_request.timeout > timezone.now()
        ):
            # Finished by polling, deleted, or not expired yet
            return

        backend = get_backend()
        if backend is None:
            # Signing was disabled in the meantime
            return

        backend.cancel_signature(signature_request)
        signature_request.save()
        logger.info(
            "Signature request %s ended with status %s",
            signature_request.pk,
            signature_request.status,
        )

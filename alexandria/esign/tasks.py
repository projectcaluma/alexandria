from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone

from alexandria.esign import api
from alexandria.esign.models import SignatureRequest
from celery import shared_task

logger = get_task_logger(__name__)


@shared_task
def cancel_expired_signature_request(signature_request_pk: str):
    """Clean up a request the frontend stopped polling.

    Scheduled for the timeout of the request. Fetches the final state once
    more (the user may have confirmed in the meantime), otherwise ends the
    request and drops the prepared PDF. Expired requests are also ended when
    someone starts a new request for the file, in case this task never runs.
    """
    with transaction.atomic():
        signature_request = (
            SignatureRequest.objects.select_for_update()
            .filter(pk=signature_request_pk)
            .first()
        )
        if signature_request is None or not signature_request.is_active:
            # Finished by polling or deleted
            return

        if signature_request.timeout and signature_request.timeout > timezone.now():
            # Ran early (e.g. clock skew between workers), try again later
            cancel_expired_signature_request.apply_async_on_commit(
                args=[signature_request_pk], eta=signature_request.timeout
            )
            return

        api.end_expired_request(signature_request)
        logger.info(
            "Signature request %s ended with status %s",
            signature_request.pk,
            signature_request.status,
        )

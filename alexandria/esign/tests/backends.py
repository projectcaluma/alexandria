from datetime import timedelta

from django.utils import timezone

from alexandria.esign.backends.base import SignatureBackend
from alexandria.esign.models import Signature, SignatureRequest


class FakeBackend(SignatureBackend):
    enabled_groups = {"admin"}
    stamp_type = Signature.Type.TIMESTAMP

    def is_enabled_for(self, group):
        return group in self.enabled_groups

    def request_signature(self, signature_request):
        signature_request.signature_type = SignatureRequest.Type.QUALIFIED
        signature_request.status = SignatureRequest.Status.REQUESTED
        signature_request.provider_reference = "fake-ref"
        signature_request.action_url = "https://signing.example.com/fake-ref"
        signature_request.timeout = timezone.now() + timedelta(minutes=2)

    def poll_signature(self, signature_request):
        signature_request.status = SignatureRequest.Status.DONE
        signature_request.provider_status = "signed"

    def cancel_signature(self, signature_request):
        signature_request.status = SignatureRequest.Status.TIMEOUT

    def stamp(self, file, user, group, data):
        return Signature.objects.create(
            file=file,
            signature_type=self.stamp_type,
            signer_name="Fake Seal",
            signed_at=timezone.now(),
            signature_hash="fake-hash",
            created_by_user=user,
            created_by_group=group,
        )

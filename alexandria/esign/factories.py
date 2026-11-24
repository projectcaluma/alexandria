from django.utils import timezone
from factory import Faker, LazyFunction, SubFactory

from alexandria.core.factories import BaseFactory, FileFactory

from . import models


class SignatureRequestFactory(BaseFactory):
    file = SubFactory(FileFactory, mime_type="application/pdf")

    class Meta:
        model = models.SignatureRequest


class SignatureFactory(BaseFactory):
    file = SubFactory(FileFactory, mime_type="application/pdf")
    signature_type = models.Signature.Type.QUALIFIED
    signer_name = Faker("name")
    signed_at = LazyFunction(timezone.now)
    signature_hash = Faker("sha256")

    class Meta:
        model = models.Signature

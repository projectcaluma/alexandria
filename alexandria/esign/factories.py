from django.utils import timezone
from factory import Faker, LazyFunction, SubFactory

from alexandria.core.factories import BaseFactory, FileFactory

from . import models


class SignatureProviderCredentialsFactory(BaseFactory):
    group = "admin"
    account_id = Faker("uuid4")
    username = Faker("user_name")
    password = Faker("password")

    class Meta:
        model = models.SignatureProviderCredentials
        django_get_or_create = ("group",)


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

import base64
from datetime import timedelta
from io import BytesIO

import pytest
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image
from pyhanko.pdf_utils.reader import PdfFileReader

from alexandria.core.models import File
from alexandria.esign import pdf
from alexandria.esign.backends.base import SignatureProviderError
from alexandria.esign.backends.deepsign import DeepSignBackend
from alexandria.esign.dev import example_stamp_data
from alexandria.esign.models import Signature, SignatureRequest

TOKEN_URL = "https://deepsign.example.com/token"
GATEWAY_URL = "https://deepsign.example.com/gateway"
SIGN_URL = "https://deepsign.example.com/sign"


@pytest.fixture(autouse=True)
def deepsign_api(settings, requests_mock):
    settings.ALEXANDRIA_DEEPSIGN_TOKEN_URL = TOKEN_URL
    settings.ALEXANDRIA_DEEPSIGN_GATEWAY_URL = GATEWAY_URL
    settings.ALEXANDRIA_DEEPSIGN_SIGN_URL = SIGN_URL
    settings.ALEXANDRIA_DEEPSIGN_SIGNATURE_BYTES_RESERVED = 16384
    settings.ALEXANDRIA_DEEPSIGN_STAMP_DATA_FUNCTION = None
    requests_mock.post(TOKEN_URL, json={"access_token": "token", "expires_in": 900})
    requests_mock.post(
        f"{GATEWAY_URL}/persons/register", json={"personIdentityUid": "identity"}
    )
    requests_mock.post(
        f"{SIGN_URL}/service/hash/sign",
        json={"hashKey": "hash-key", "signStatus": "in-progress"},
    )
    return requests_mock


@pytest.fixture
def pdf_file(file_factory, pdf_content):
    return file_factory(
        name="decision.pdf",
        mime_type="application/pdf",
        content=ContentFile(pdf_content, name="decision.pdf"),
        created_by_user="admin",
        created_by_group="admin",
    )


@pytest.fixture
def started_request(
    signature_request_factory, pdf_file, deep_sign_service_account, deepsign_api
):
    signature_request = signature_request_factory(
        file=pdf_file, created_by_user="admin", created_by_group="admin"
    )
    DeepSignBackend().request_signature(signature_request)
    signature_request.save()
    return signature_request


def _mock_status(deepsign_api, status, signature=None):
    body = {"signStatus": status}
    if signature:
        body["signatureData"] = {
            "signatures": [{"signature": base64.b64encode(signature).decode()}]
        }
    deepsign_api.get(f"{SIGN_URL}/service/hash/hash-key/status", json=body)


@pytest.mark.django_db
def test_start(started_request, deepsign_api):
    assert started_request.status == SignatureRequest.Status.REQUESTED
    assert started_request.signature_type == SignatureRequest.Type.QUALIFIED
    assert started_request.provider_reference == "hash-key"
    assert started_request.provider_status == "in-progress"
    assert started_request.timeout > timezone.now()
    assert started_request.prepared_content

    sign_body = deepsign_api.request_history[-1].json()
    digest = pdf.deserialize_digest(started_request.provider_data["digest"])
    assert (
        sign_body["hashes"][0]["digestValue"]
        == base64.b64encode(digest.document_digest).decode()
    )
    assert sign_body["didIdentityId"] == "identity"
    assert sign_body["documentName"] == "decision.pdf"

    register_body = deepsign_api.request_history[1].json()
    assert register_body == {"personRef": "alexandria-admin"}


@pytest.mark.django_db
def test_start_registration_required(
    signature_request_factory, deep_sign_service_account, deepsign_api
):
    deepsign_api.post(
        f"{GATEWAY_URL}/persons/register",
        json={"registrationDeepLink": "https://deepid.example.com/register"},
    )
    signature_request = signature_request_factory(created_by_group="admin")

    DeepSignBackend().request_signature(signature_request)

    assert signature_request.status == SignatureRequest.Status.REGISTRATION_REQUIRED
    assert signature_request.action_url == "https://deepid.example.com/register"
    assert not signature_request.is_active


@pytest.mark.django_db
def test_poll_signed(started_request, deepsign_api, sign_digest):
    digest = pdf.deserialize_digest(started_request.provider_data["digest"])
    signature = sign_digest(digest.document_digest)
    _mock_status(deepsign_api, "signed", signature)

    DeepSignBackend().poll_signature(started_request)

    assert started_request.status == SignatureRequest.Status.DONE
    assert started_request.prepared_content is None

    result = Signature.objects.get()
    assert result.signature_request == started_request
    assert result.signature_type == Signature.Type.QUALIFIED
    assert result.signer_name == "Winston Smith"

    signed_file = result.file
    assert signed_file != started_request.file
    assert signed_file.document == started_request.file.document
    assert signed_file.variant == File.Variant.ORIGINAL
    assert signed_file.name == "decision.pdf"
    assert pdf.last_signature(signed_file.content.read()).signer_name == (
        "Winston Smith"
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "provider_status,timeout_delta,expected_status",
    [
        ("in-progress", timedelta(minutes=1), SignatureRequest.Status.REQUESTED),
        ("in-progress", timedelta(minutes=-1), SignatureRequest.Status.TIMEOUT),
        ("rejected", timedelta(minutes=1), SignatureRequest.Status.REJECTED),
    ],
)
def test_poll(
    started_request, deepsign_api, provider_status, timeout_delta, expected_status
):
    _mock_status(deepsign_api, provider_status)
    started_request.timeout = timezone.now() + timeout_delta

    DeepSignBackend().poll_signature(started_request)

    assert started_request.status == expected_status
    assert started_request.provider_status == provider_status
    assert (started_request.prepared_content is None) == (not started_request.is_active)
    assert not Signature.objects.exists()


@pytest.mark.django_db
def test_cancel(started_request, deepsign_api):
    _mock_status(deepsign_api, "in-progress")

    DeepSignBackend().cancel_signature(started_request)

    assert started_request.status == SignatureRequest.Status.TIMEOUT
    assert started_request.prepared_content is None


@pytest.mark.django_db
def test_cancel_signed_in_the_meantime(started_request, deepsign_api, sign_digest):
    digest = pdf.deserialize_digest(started_request.provider_data["digest"])
    _mock_status(deepsign_api, "signed", sign_digest(digest.document_digest))

    DeepSignBackend().cancel_signature(started_request)

    assert started_request.status == SignatureRequest.Status.DONE
    assert Signature.objects.exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "mock_kwargs",
    [
        {"status_code": 500},
        {"text": "no json"},
        {"json": {"signStatus": "in-progress"}},
    ],
)
def test_start_provider_error(
    signature_request_factory,
    pdf_file,
    deep_sign_service_account,
    deepsign_api,
    mock_kwargs,
):
    deepsign_api.post(f"{SIGN_URL}/service/hash/sign", **mock_kwargs)
    signature_request = signature_request_factory(
        file=pdf_file, created_by_group="admin"
    )

    with pytest.raises(SignatureProviderError):
        DeepSignBackend().request_signature(signature_request)


@pytest.mark.django_db
def test_authentication_error(
    signature_request_factory, deep_sign_service_account, deepsign_api
):
    deepsign_api.post(TOKEN_URL, status_code=401)
    signature_request = signature_request_factory(created_by_group="admin")

    with pytest.raises(SignatureProviderError):
        DeepSignBackend().request_signature(signature_request)


@pytest.mark.django_db
def test_poll_signed_without_signature(started_request, deepsign_api):
    _mock_status(deepsign_api, "signed")

    with pytest.raises(SignatureProviderError):
        DeepSignBackend().poll_signature(started_request)


@pytest.mark.django_db
def test_access_token_is_reused(started_request, deepsign_api):
    _mock_status(deepsign_api, "in-progress")

    DeepSignBackend().poll_signature(started_request)
    DeepSignBackend().poll_signature(started_request)

    token_requests = [r for r in deepsign_api.request_history if r.url == TOKEN_URL]
    assert len(token_requests) == 1
    assert token_requests[0].text and "grant_type=password" in token_requests[0].text


def _stamp_response(timestamp_token, status="signed"):
    """Timestamp the digest DeepSign receives, like the real API."""

    def callback(request, context):
        digest = base64.b64decode(request.json()["hashes"][0]["digestValue"])
        return {
            "hashKey": "hash-key",
            "signStatus": status,
            "signatureData": {
                "signatures": [
                    {"signature": base64.b64encode(timestamp_token(digest)).decode()}
                ]
            },
        }

    return callback


@pytest.mark.django_db
def test_stamp(pdf_file, deep_sign_service_account, deepsign_api, timestamp_token):
    deepsign_api.post(
        f"{SIGN_URL}/service/hash/sign", json=_stamp_response(timestamp_token)
    )

    result = DeepSignBackend().stamp(pdf_file, user="admin", group="admin", data={})

    sign_body = deepsign_api.request_history[-1].json()
    assert sign_body["signatureMode"] == "timestamp"
    assert "didIdentityId" not in sign_body
    # No DeepID identity needed
    assert not any("persons/register" in r.url for r in deepsign_api.request_history)

    assert result.signature_type == Signature.Type.TIMESTAMP
    assert result.signature_request is None
    assert result.created_by_user == "admin"
    assert result.file != pdf_file
    assert result.file.document == pdf_file.document
    stamped = result.file.content.read()
    embedded = PdfFileReader(BytesIO(stamped)).embedded_signatures[-1]
    assert embedded.sig_object_type == "/DocTimeStamp"
    assert pdf.last_signature(stamped).signer_name == "Winston Smith"


@pytest.mark.django_db
def test_stamp_polls_status(
    mocker, pdf_file, deep_sign_service_account, deepsign_api, timestamp_token
):
    sleep = mocker.patch("alexandria.esign.backends.deepsign.time.sleep")
    signed = {}

    def sign_callback(request, context):
        signed.update(_stamp_response(timestamp_token)(request, context))
        return {"hashKey": "hash-key", "signStatus": "in-progress"}

    deepsign_api.post(f"{SIGN_URL}/service/hash/sign", json=sign_callback)
    deepsign_api.get(
        f"{SIGN_URL}/service/hash/hash-key/status", json=lambda *_args: signed
    )

    result = DeepSignBackend().stamp(pdf_file, user="admin", group="admin", data={})

    assert result.signature_type == Signature.Type.TIMESTAMP
    assert sleep.call_count == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "sign_response",
    [
        {"hashKey": "hash-key", "signStatus": "rejected"},
        {"signStatus": "in-progress"},
    ],
)
def test_stamp_not_signed(
    mocker, pdf_file, deep_sign_service_account, deepsign_api, sign_response
):
    mocker.patch("alexandria.esign.backends.deepsign.time.sleep")
    deepsign_api.post(f"{SIGN_URL}/service/hash/sign", json=sign_response)

    with pytest.raises(SignatureProviderError):
        DeepSignBackend().stamp(pdf_file, user="admin", group="admin", data={})

    assert not Signature.objects.exists()


@pytest.mark.django_db
def test_stamp_status_never_signed(
    mocker, pdf_file, deep_sign_service_account, deepsign_api
):
    sleep = mocker.patch("alexandria.esign.backends.deepsign.time.sleep")
    _mock_status(deepsign_api, "in-progress")

    with pytest.raises(SignatureProviderError):
        DeepSignBackend().stamp(pdf_file, user="admin", group="admin", data={})

    assert sleep.call_count == 5


@pytest.mark.django_db
def test_stamp_with_image(
    pdf_file, deep_sign_service_account, deepsign_api, timestamp_token, test_signer
):
    deepsign_api.post(
        f"{SIGN_URL}/service/hash/sign", json=_stamp_response(timestamp_token)
    )
    image = BytesIO()
    Image.new("RGB", (60, 40), (0, 128, 0)).save(image, format="PNG")

    result = DeepSignBackend().stamp(
        pdf_file,
        user="admin",
        group="admin",
        data={"image": image.getvalue(), "text": "17.11.2026"},
    )

    reader = PdfFileReader(BytesIO(result.file.content.read()))
    stamp = reader.embedded_signatures[-1]
    assert stamp.sig_object_type == "/DocTimeStamp"
    # Visible at the configured position, covered by the timestamp
    assert [float(v) for v in stamp.sig_field["/Rect"]] == [415, 722, 565, 812]
    assert "/N" in stamp.sig_field["/AP"]
    # Long-term validation info
    assert len(reader.root["/DSS"]["/Certs"]) == 1


def stamp_data(file, user, group):
    return {"image": example_stamp_data(file, user, group)["image"], "text": group}


@pytest.mark.django_db
def test_stamp_data_function(
    settings, pdf_file, deep_sign_service_account, deepsign_api, timestamp_token
):
    settings.ALEXANDRIA_DEEPSIGN_STAMP_DATA_FUNCTION = (
        "alexandria.esign.tests.test_deepsign_backend.stamp_data"
    )
    deepsign_api.post(
        f"{SIGN_URL}/service/hash/sign", json=_stamp_response(timestamp_token)
    )

    result = DeepSignBackend().stamp(pdf_file, user="admin", group="admin", data={})

    stamp = PdfFileReader(BytesIO(result.file.content.read())).embedded_signatures[-1]
    assert [float(v) for v in stamp.sig_field["/Rect"]] == [415, 722, 565, 812]

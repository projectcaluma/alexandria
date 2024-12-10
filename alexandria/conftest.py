import importlib
import inspect
import io
import json
import shutil
import sys
from pathlib import Path

import pytest
from django.apps import apps
from django.core.cache import cache
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from pytest_factoryboy.fixture import Box
from rest_framework.test import APIClient

from alexandria.core import tasks
from alexandria.oidc_auth.models import OIDCUser


def register_module(module):
    # We need to pass the locals of this file to the register method to make
    # sure they are injected on the conftest locals instead of the default
    # locals which would be the locals of this function
    conftest_locals = Box(sys._getframe(1).f_locals)

    for _, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            register(obj, _caller_locals=conftest_locals)


register_module(importlib.import_module(".core.factories", "alexandria"))


@pytest.fixture(autouse=True)
def _default_file_storage_backend(settings):
    settings.ALEXANDRIA_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = False


@pytest.fixture(autouse=True)
def _make_clean_media_dir(settings):
    test_media_root = Path(settings.MEDIA_ROOT) / "test"
    test_media_root.mkdir(parents=True, exist_ok=True)
    settings.MEDIA_ROOT = str(test_media_root)
    pytest.yield_fixture
    shutil.rmtree(test_media_root)


@pytest.fixture(autouse=True)
def mock_tika(mocker):
    mocker.patch("tika.parser.from_buffer", return_value={"content": "Important text"})
    mocker.patch("tika.language.from_buffer", return_value="en")


@pytest.fixture(autouse=True)
def mock_celery(mocker):
    mocker.patch("django.db.transaction.on_commit", side_effect=lambda f: f())
    mocker.patch(
        "alexandria.core.tasks.set_checksum.delay",
        side_effect=lambda id: tasks.set_checksum(id),
    )
    mocker.patch(
        "alexandria.core.tasks.set_content_vector.delay",
        side_effect=lambda id, b=False: tasks.set_content_vector(id, b),
    )
    mocker.patch(
        "alexandria.core.tasks.create_thumbnail.delay",
        side_effect=lambda id: tasks.create_thumbnail(id),
    )


@pytest.fixture
def admin_groups():
    return ["admin"]


@pytest.fixture
def user(settings, admin_groups):
    return OIDCUser(
        "sometoken",
        {settings.OIDC_USERNAME_CLAIM: "user", settings.OIDC_GROUPS_CLAIM: ["group"]},
    )


@pytest.fixture
def admin_user(settings, admin_groups):
    return OIDCUser(
        "sometoken",
        {
            settings.OIDC_USERNAME_CLAIM: "admin",
            settings.OIDC_GROUPS_CLAIM: admin_groups,
        },
    )


@pytest.fixture
def client(db):
    client = APIClient()
    return client


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture(scope="function", autouse=True)
def _autoclear_cache():
    cache.clear()


@pytest.fixture(autouse=True)
def reset_config_classes(settings):
    """
    Reset the config classes to clean state after test.

    The config classes need to be reset after running tests that
    use them. Otherwise, unrelated tests may get affected.
    """

    # First, set config to original value
    core_config = apps.get_app_config("generic_permissions")
    core_config.ready()


@pytest.fixture()
def manabi(settings):
    settings.ALEXANDRIA_USE_MANABI = True


@pytest.fixture()
def document_post_data(category):
    content = io.BytesIO(
        b"%PDF-1.\ntrailer<</Root<</Pages<</Kids[<</MediaBox[0 0 3 3]>>]>>>>>>"
    )
    content.name = "foo.pdf"
    return {
        "content": content,
        "data": io.BytesIO(
            json.dumps({"title": "winstonsmith", "category": category.pk}).encode(
                "utf-8"
            )
        ),
    }

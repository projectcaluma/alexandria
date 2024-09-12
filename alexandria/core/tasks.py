import hashlib
from pathlib import Path

import tika.language
import tika.parser
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.db.models import Value

from alexandria.core.models import File
from celery import shared_task


@shared_task(soft_time_limit=301)
def set_content_vector(file_pk: str):
    file = File.objects.get(pk=file_pk)
    file.content.file.file.seek(0)

    # tika has an internal time limit of 300s, set the request limit to match that
    # different values should be set in tika as well
    # https://github.com/CogStack/tika-service/blob/master/README.md#tika-parsers-configuration
    parsed_content = tika.parser.from_buffer(
        file.content.file.file, requestOptions={"timeout": 300}
    )

    name_vector = SearchVector(Value(Path(file.name).stem), weight="A")
    if not parsed_content["content"]:
        # Update only content_vector, to avoid race conditions
        File.objects.filter(pk=file.pk).update(content_vector=name_vector)
        return

    # use part of content for language detection, beacause metadata is not reliable
    language = tika.language.from_buffer(parsed_content["content"][:1000])
    config = settings.ALEXANDRIA_ISO_639_TO_PSQL_SEARCH_CONFIG.get(language, "simple")
    content_vector = name_vector + SearchVector(
        Value(parsed_content["content"].strip()),
        config=config,
        weight="B",
    )

    # Update only need fields, to avoid race conditions
    File.objects.filter(pk=file.pk).update(
        content_vector=content_vector, language=language
    )


@shared_task
def set_checksum(file_pk: str):
    file = File.objects.get(pk=file_pk)
    file.content.file.file.seek(0)
    checksum = make_checksum(file.content.file.file.read())

    # Update only checksum, to avoid race conditions
    File.objects.filter(pk=file.pk).update(checksum=checksum)


def make_checksum(bytes_: bytes) -> str:
    return f"sha256:{hashlib.sha256(bytes_).hexdigest()}"

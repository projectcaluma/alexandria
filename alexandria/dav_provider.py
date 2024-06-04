import io
import time
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.base import File as DjangoFile
from manabi.filesystem import ManabiFileResourceMixin, ManabiProvider
from wsgidav.dav_error import HTTP_FORBIDDEN, DAVError
from wsgidav.dav_provider import DAVNonCollection

from alexandria.core.validations import validate_file


class MyBytesIO(io.BytesIO):
    """
    Custom BytesIO.

    We're writing the DAV-file into a `BytesIO`, so we can perform the actual saving in
    `AlexandriaFileResource.end_write()`. This is needed, to make sure the file is
    scanned for viruses and encrypted in storage, if one of those features is enabled.
    `wsgidav.RequestServer.do_PUT` would close the file after writing, thus making its
    content unavailable in `AlexandriaFileResource.end_write()`. This class just
    overrides the `close()`-method in order to prevent closing. Afterward, we have to
    manually call `.do_close()` to clean up.
    """

    def close(self):
        # prevent closing the file
        return

    def do_close(self):
        return super().close()


class AlexandriaFileResource(ManabiFileResourceMixin, DAVNonCollection):
    def __init__(
        self,
        path,
        environ,
        *,
        cb_hook_config=None,
    ):
        # Lazy import to avoid not ready app
        global File
        from alexandria.core.models import File

        self.provider: AlexandriaProvider
        super().__init__(path, environ)
        self._cb_config = cb_hook_config
        self._token = environ["manabi.token"]
        self.user, self.group, file_pk = self._token.payload

        # We only serve the newest original File of the Document.
        self.file = (
            File.objects.get(pk=file_pk)
            .document.files.filter(variant=File.Variant.ORIGINAL)
            .order_by("-created_at")
            .first()
        )
        self.memory_file = MyBytesIO()
        self.name = Path(self.path).name

    def _get_timestamp(self, dt):
        return time.mktime(dt.timetuple())

    def support_etag(self):
        # we only support etag with S3Storage
        if hasattr(self.file.content.file, "obj"):
            return True

    def get_content_length(self):
        return self.file.size

    def get_content_type(self):
        return self.file.mime_type

    def get_creation_date(self):
        return self._get_timestamp(self.file.created_at)

    def get_etag(self):
        if self.support_etag():
            return self.file.content.file.obj.e_tag.strip('"')

    def get_last_modified(self):
        return self._get_timestamp(self.file.modified_at)

    def get_content(self):
        assert not self.is_collection
        return self.file.content.file

    def begin_write(self, *, content_type=None):
        self.process_pre_write_hooks()
        assert not self.is_collection
        if self.provider.readonly:  # pragma: no cover
            raise DAVError(HTTP_FORBIDDEN)
        return self.memory_file

    def end_write(self, *, with_errors):
        file = self.file
        if (
            self.file.modified_by_user != self.user
            or self.file.modified_by_group != self.group
        ):
            file = File(
                variant=self.file.variant,
                original=self.file.original,
                name=self.file.name,
                document=self.file.document,
                encryption_status=self.file.encryption_status,
                mime_type=self.file.mime_type,
                created_by_user=self.user,
                created_by_group=self.group,
                modified_by_user=self.user,
                modified_by_group=self.group,
            )
        file.size = self.memory_file.getbuffer().nbytes
        self.memory_file.seek(0)
        django_file = DjangoFile(name=file.name, file=self.memory_file)
        file.content = django_file

        try:
            validate_file(file)
        except ValidationError:
            raise DAVError(HTTP_FORBIDDEN)

        file.save()
        self.file = file
        self.memory_file.do_close()
        super().end_write(with_errors=with_errors)


class AlexandriaProvider(ManabiProvider):
    def get_file_resource(self, path, environ, _):
        try:
            return AlexandriaFileResource(
                path,
                environ,
                cb_hook_config=self._cb_hook_config,
            )
        except File.DoesNotExist:
            return None

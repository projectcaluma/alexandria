import io
import itertools
import logging
import zipfile
from os.path import splitext
from tempfile import NamedTemporaryFile

import requests
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoCoreValidationError
from django.core.files.base import ContentFile
from django.http import FileResponse
from django.utils.translation import gettext as _
from generic_permissions.permissions import AllowAny, PermissionViewMixin
from generic_permissions.visibilities import VisibilityViewMixin
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    ModelViewSet,
    PreloadIncludesMixin,
    RelatedMixin,
)

from . import models, serializers
from .filters import (
    CategoryFilterSet,
    DocumentFilterSet,
    FileFilterSet,
    MarkFilterSet,
    TagFilterSet,
)
from .presign_urls import verify_signed_components

log = logging.getLogger(__name__)


class CategoryViewSet(
    PermissionViewMixin,
    VisibilityViewMixin,
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    filterset_class = CategoryFilterSet
    select_for_includes = {"parent": ["parent"]}
    prefetch_for_includes = {"children": ["children"]}

    def perform_destroy(self, instance):
        # needed for DGAP
        raise NotImplementedError(_("Deleting categories over API is not supported."))

    def create(self, request, *args, **kwargs):
        # needed for DGAP
        raise NotImplementedError(_("Creating categories over API is not supported."))


class TagSynonymGroupViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TagSynonymGroupSerializer
    queryset = models.TagSynonymGroup.objects.all().distinct()


class TagViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all().distinct()
    filterset_class = TagFilterSet
    search_fields = ("name", "description")
    select_for_includes = {"tag_synonym_group": ["tag_synonym_group"]}


class MarkViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.MarkSerializer
    queryset = models.Mark.objects.all().distinct()
    filterset_class = MarkFilterSet


class DocumentViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()
    filterset_class = DocumentFilterSet
    search_fields = ("title", "files__name", "tags__name", "description")
    select_for_includes = {"category": ["category"]}
    prefetch_for_includes = {"tags": ["tags"], "files": ["files"]}

    def update(self, request, *args, **kwargs):
        """Override so we can delete unused tags."""
        response = super().update(request, *args, **kwargs)
        models.Tag.objects.all().filter(documents__pk__isnull=True).delete()

        return response

    @action(methods=["post"], detail=True)
    def convert(self, request, pk=None):
        if not settings.ALEXANDRIA_ENABLE_PDF_CONVERSION:
            raise ValidationError(_("PDF conversion is not enabled."))

        document = self.get_object()
        file = document.get_latest_original()

        response = requests.post(
            settings.ALEXANDRIA_DMS_URL + "/convert",
            data={"target_format": "pdf"},
            headers={"authorization": get_authorization_header(request)},
            files={"file": file.content},
        )

        if response.status_code == HTTP_401_UNAUTHORIZED:
            raise AuthenticationFailed(response.json().get("detail"))

        response.raise_for_status()

        username = serializers.default_user_attribute(
            request.user, settings.ALEXANDRIA_CREATED_BY_USER_PROPERTY
        )
        group = serializers.default_user_attribute(
            request.user, settings.ALEXANDRIA_CREATED_BY_GROUP_PROPERTY
        )

        converted_document = models.Document.objects.create(
            title={k: f"{ splitext(v)[0]}.pdf" for k, v in document.title.items()},
            description=document.description,
            category=document.category,
            date=document.date,
            metainfo=document.metainfo,
            created_by_user=username,
            created_by_group=group,
            modified_by_user=username,
            modified_by_group=group,
        )
        file_name = f"{splitext(file.name)[0]}.pdf"
        converted_file = models.File.objects.create(
            document=converted_document,
            name=file_name,
            content=ContentFile(response.content, file_name),
            mime_type="application/pdf",
            size=len(response.content),
            metainfo=file.metainfo,
            created_by_user=username,
            created_by_group=group,
            modified_by_user=username,
            modified_by_group=group,
        )
        converted_file.create_thumbnail()

        serializer = self.get_serializer(converted_document)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class FileViewSet(
    PermissionViewMixin,
    VisibilityViewMixin,
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.FileSerializer

    queryset = models.File.objects.all()
    filterset_class = FileFilterSet
    select_for_includes = {"document": ["document"], "original": ["original"]}
    prefetch_for_includes = {"renderings": ["renderings"]}

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"view": self, "request": self.request})
        return context

    def _write_zip(self, file_obj, queryset):
        with zipfile.ZipFile(file_obj, "w", zipfile.ZIP_DEFLATED) as zipf:
            seen_names = set()
            for _file in queryset.order_by("-name").iterator():
                temp_file = io.BytesIO()
                temp_file.write(_file.content.file.file.read())

                temp_file.seek(0)

                name = _file.name
                suffixes = itertools.count(start=1)
                while name in seen_names:
                    (base_name, *maybe_ext) = _file.name.rsplit(".", 1)
                    # extension is now a 0- or 1-sized list
                    extension = f".{maybe_ext[0]}" if maybe_ext else ""
                    name = f"{base_name}({next(suffixes)}){extension}"
                seen_names.add(name)

                zipf.writestr(
                    name,
                    temp_file.read(),
                )
        file_obj.seek(0)
        return file_obj

    @action(methods=["get"], detail=False)
    def multi(self, request, **kwargs):
        if not request.query_params.get("filter[files]"):
            raise ValidationError(_('Specifying a "files" filter is mandatory!'))

        try:
            queryset = self.filter_queryset(self.get_queryset())
        except DjangoCoreValidationError as exp:
            raise ValidationError(*exp.messages)

        try:
            if not queryset:
                raise NotFound()
        except DjangoCoreValidationError:  # pragma: todo cover
            raise ValidationError(
                _(
                    'The "files" filter must consist of a comma delimited list of '
                    "File PKs!"
                )
            )

        with NamedTemporaryFile() as file_obj:
            file_obj = self._write_zip(file_obj, queryset)
            response = FileResponse(
                open(file_obj.name, "rb"),
                content_type="application/zip",
                filename="files.zip",
            )

            return response

    def create(self, request, *args, **kwargs):
        # invoke dgap permission check
        self._check_permissions(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION:
            serializer.validated_data["encryption_status"] = (
                settings.ALEXANDRIA_ENCRYPTION_METHOD
            )
        obj = serializer.save()
        if obj.variant == models.File.Variant.ORIGINAL:
            try:
                obj.create_thumbnail()
            except DjangoCoreValidationError as e:
                log.error(
                    "Object {obj} created successfully. Thumbnail creation failed. Error: {error}".format(
                        obj=obj, error=e.messages
                    )
                )
        if obj.variant == models.File.Variant.THUMBNAIL:
            try:
                # coerce the uploaded file to a thumbnail
                obj.create_thumbnail()
            except DjangoCoreValidationError as e:
                # remove the uploaded file on failure to avoid
                # collsions
                obj.delete()
                raise ValidationError(*e.messages)
            # if the original already had a thumbnail remove that
            self.queryset.filter(original=obj.original).exclude(pk=obj.pk).delete()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    @permission_classes([AllowAny])
    @action(methods=["get"], detail=True)
    def download(self, request, pk=None):
        if token_sig := request.query_params.get("signature"):
            verify_signed_components(
                pk,
                request.get_host(),
                expires=int(request.query_params.get("expires")),
                scheme=request.META.get("wsgi.url_scheme", "http"),
                token_sig=token_sig,
            )
            obj = models.File.objects.get(pk=pk)

            return FileResponse(
                obj.content.file.file, as_attachment=False, filename=obj.name
            )
        raise PermissionDenied("For downloading a file use the presigned download URL.")

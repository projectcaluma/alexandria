import io
import itertools
import logging
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

import requests
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoCoreValidationError
from django.core.files.base import ContentFile
from django.http import FileResponse
from django.utils.translation import gettext as _
from django_presigned_url.presign_urls import verify_presigned_request
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
from rest_framework_json_api.relations import reverse
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    ModelViewSet,
    PreloadIncludesMixin,
    RelatedMixin,
)

from alexandria.core.utils import get_user_and_group_from_request

from . import models, serializers
from .api import copy_document, create_document_file
from .filters import (
    CategoryFilterSet,
    DocumentFilterSet,
    FileFilterSet,
    MarkFilterSet,
    SearchFilterSet,
    TagFilterSet,
)
from .tasks import set_content_vector

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
    prefetch_for_includes = {
        "__all__": ["children"],
        "children": ["children__parent"],
    }


class TagSynonymGroupViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TagSynonymGroupSerializer
    queryset = models.TagSynonymGroup.objects.all().distinct()
    prefetch_for_includes = {
        "__all__": ["tags"],
    }


class TagViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all().distinct()
    filterset_class = TagFilterSet
    search_fields = ("name", "description")
    prefetch_for_includes = {"tag_synonym_group": ["tag_synonym_group__tags"]}
    ordering_fields = "__all__"
    ordering = ["name"]


class MarkViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.MarkSerializer
    queryset = models.Mark.objects.all().distinct()
    filterset_class = MarkFilterSet


class DocumentViewSet(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()
    filterset_class = DocumentFilterSet
    select_for_includes = {"category": ["category__parent"]}
    prefetch_for_includes = {
        "__all__": ["marks", "tags", "files"],
        "files": ["files__renderings", "files__original"],
        "category": ["category__children"],
    }

    def update(self, request, *args, **kwargs):
        document = self.get_object()
        update_content_vector = settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH and (
            (request.data.get("title") != document.title)
            or (request.data.get("description") != document.description)
        )

        response = super().update(request, *args, **kwargs)
        models.Tag.objects.all().filter(documents__pk__isnull=True).delete()

        if update_content_vector and document.files.count():
            set_content_vector.delay_on_commit(document.get_latest_original().pk, True)

        return response

    @action(
        methods=["post"],
        detail=True,
        url_path="copy",
    )
    def copy(self, request, pk=None):
        document = self.get_object()
        user, group = get_user_and_group_from_request(request)

        copy_request_serializer = serializers.CopyRequestSerializer(data=request.data)
        copy_request_serializer.is_valid(raise_exception=True)
        category = (
            copy_request_serializer.validated_data.get("category", False)
            or document.category
        )

        copied_document = copy_document(
            document=document,
            category=category,
            user=user,
            group=group,
        )

        serializer = self.get_serializer(copied_document)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

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

        user, group = get_user_and_group_from_request(request)

        file_name = f"{Path(file.name).stem}.pdf"
        document_title = f"{Path(document.title).stem}.pdf"
        converted_document, __ = create_document_file(
            user=user,
            group=group,
            category=document.category,
            document_title=document_title,
            file_name=file_name,
            file_content=ContentFile(response.content, file_name),
            mime_type="application/pdf",
            file_size=len(response.content),
            additional_document_attributes={
                "description": document.description,
                "date": document.date,
                "metainfo": document.metainfo,
            },
            additional_file_attributes={
                "metainfo": file.metainfo,
            },
        )

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
    prefetch_for_includes = {
        "__all__": ["renderings"],
        "document": ["document__marks", "document__tags", "document__files"],
    }

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"view": self, "request": self.request})
        return context

    def _write_zip(self, file_obj, queryset):
        with zipfile.ZipFile(file_obj, "w", zipfile.ZIP_DEFLATED) as zipf:
            seen_names = set()
            for _file in queryset.order_by("-name").iterator(chunk_size=50):
                temp_file = io.BytesIO()
                temp_file.write(_file.content.file.file.read())

                temp_file.seek(0)

                suffixes = itertools.count(start=1)
                base_name, extension = _file.get_download_filename()

                name = f"{base_name}{extension}"
                while name in seen_names:
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
            raise ValidationError(_('"files" filter is mandatory!'))

        try:
            queryset = self.filter_queryset(self.get_queryset())
        except DjangoCoreValidationError as exp:
            raise ValidationError(*exp.messages)

        try:
            if not queryset:
                raise NotFound()
        except DjangoCoreValidationError:  # pragma: todo cover
            raise ValidationError(
                _('The "files" filter must consist of a comma delimited list of UUIDs!')
            )

        with NamedTemporaryFile() as file_obj:
            file_obj = self._write_zip(file_obj, queryset)
            response = FileResponse(
                open(file_obj.name, "rb"),
                content_type="application/zip",
                filename="files.zip",
            )

            return response

    @permission_classes([AllowAny])
    @action(methods=["get"], detail=True)
    def download(self, request, pk=None):
        try:
            if not verify_presigned_request(
                reverse("file-download", args=[pk]), request
            ):
                raise PermissionDenied(
                    _("For downloading a file use the presigned download URL.")
                )
        except DjangoCoreValidationError as exp:
            raise PermissionDenied(*exp.messages)

        obj = models.File.objects.get(pk=pk)

        unsafe = obj.mime_type not in settings.SAFE_FOR_INLINE_DISPOSITION
        base_name, extension = obj.get_download_filename()

        return FileResponse(
            obj.content.file.file,
            as_attachment=unsafe,
            filename=f"{base_name}{extension}",
            content_type=obj.mime_type,
        )


class WebDAVViewSet(
    PermissionViewMixin,
    VisibilityViewMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.WebDAVSerializer
    queryset = models.Document.objects.all()

    def check_permissions(self, request):
        if not settings.ALEXANDRIA_USE_MANABI:
            raise NotFound(_("WebDAV is not enabled."))
        # call DGAP
        self._check_permissions(request)
        super().check_permissions(request)

    def check_object_permissions(self, request, instance):
        if (
            instance.get_latest_original().mime_type
            not in settings.ALEXANDRIA_MANABI_ALLOWED_MIMETYPES
        ):
            raise NotFound(_("WebDAV is not enabled for this mime type."))
        # call DGAP
        self._check_object_permissions(request, instance)
        super().check_object_permissions(request, instance)


class SearchViewSet(
    PermissionViewMixin,
    VisibilityViewMixin,
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.SearchResultSerializer
    resource_name = "search-results"
    queryset = models.File.objects.all().select_related("document")
    filterset_class = SearchFilterSet

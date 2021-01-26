import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import models, serializers
from .filters import CategoryFilterSet, DocumentFilterSet, FileFilterSet, TagFilterSet
from .thumbs import create_thumbnail


class PermissionViewMixin(views.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        self.queryset.model.check_permissions(request)
        instance = self.get_object()
        instance.check_object_permissions(request)
        # we do not call `super()` in order to not fetch the object twice.
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)


class VisibilityViewMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.model.visibility_queryset_filter(queryset, self.request)


class CategoryViewSet(
    VisibilityViewMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet
):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    filterset_class = CategoryFilterSet


class TagViewSet(PermissionViewMixin, VisibilityViewMixin, views.ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all().distinct()
    filterset_class = TagFilterSet


class DocumentViewSet(PermissionViewMixin, VisibilityViewMixin, views.ModelViewSet):
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()
    filterset_class = DocumentFilterSet
    search_fields = ("title", "files__name", "tags__name", "description")


class FileViewSet(
    VisibilityViewMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.FileSerializer
    queryset = models.File.objects.all()
    filterset_class = FileFilterSet


@require_http_methods(["HEAD", "POST"])
def hook_view(request):
    if not settings.ENABLE_THUMBNAIL_GENERATION:
        return HttpResponse(status=HTTP_403_FORBIDDEN)

    if request.method == "HEAD":
        return HttpResponse(status=HTTP_200_OK)

    data = json.loads(request.body.decode("utf-8"))

    response_statuses = []
    for record in data["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        if not bucket_name == settings.MINIO_STORAGE_MEDIA_BUCKET_NAME:
            response_statuses.append(HTTP_200_OK)
            continue

        file_pk = record["s3"]["object"]["key"].split("_")[0]
        try:
            file = models.File.objects.get(pk=file_pk)
        except models.File.DoesNotExist:
            response_statuses.append(HTTP_400_BAD_REQUEST)
            continue

        if file.type == models.File.THUMBNAIL:
            response_statuses.append(HTTP_200_OK)
            continue

        created = create_thumbnail(file)
        if created is False:
            response_statuses.append(HTTP_200_OK)
            continue

        response_statuses.append(HTTP_201_CREATED)

    # Just return the highest status
    return HttpResponse(status=max(response_statuses))

from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import models, serializers
from .filters import DocumentFilterSet


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


class TagViewSet(PermissionViewMixin, VisibilityViewMixin, views.ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class DocumentViewSet(PermissionViewMixin, VisibilityViewMixin, views.ModelViewSet):
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()
    filterset_class = DocumentFilterSet


class FileViewSet(
    VisibilityViewMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.FileSerializer
    queryset = models.File.objects.all()

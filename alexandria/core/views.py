from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import models, serializers
from .filters import DocumentFilterSet


class VisibilityViewMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.model.visibility_queryset_filter(queryset, self.request)


class CategoryViewSet(
    VisibilityViewMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet
):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class TagViewSet(VisibilityViewMixin, views.ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class DocumentViewSet(VisibilityViewMixin, views.ModelViewSet):
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

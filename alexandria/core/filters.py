import json
from functools import reduce
from operator import or_

from django.conf import settings
from django.contrib.postgres.search import SearchQuery
from django.db.models import FloatField, OuterRef, Q, Subquery, TextField, Value
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast
from django_filters import (
    BaseCSVFilter,
    BaseInFilter,
    BooleanFilter,
    CharFilter,
    Filter,
    FilterSet,
)
from django_filters.constants import EMPTY_VALUES
from rest_framework.exceptions import ValidationError

from alexandria.core import models


class CharInFilter(BaseInFilter, CharFilter):
    pass


class JSONValueFilter(Filter):
    field_type_by_lookup_expr = {
        "exact": TextField,
        "gt": FloatField,
        "lt": FloatField,
        "gte": FloatField,
        "lte": FloatField,
    }

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        valid_lookups = self._valid_lookups(qs)

        try:
            value = json.loads(value)
        except json.decoder.JSONDecodeError:
            raise ValidationError("JSONValueFilter value needs to be json encoded.")

        if isinstance(value, dict):
            # be a bit more tolerant
            value = [value]

        for expr in value:
            if expr in EMPTY_VALUES:  # pragma: no cover
                continue
            if not all(("key" in expr, "value" in expr)):
                raise ValidationError(
                    'JSONValueFilter value needs to have a "key" and "value" and an '
                    'optional "lookup" key.'
                )

            lookup_expr = expr.get("lookup", self.lookup_expr)
            if lookup_expr not in valid_lookups:
                raise ValidationError(
                    f'Lookup expression "{lookup_expr}" not allowed for field '
                    f'"{self.field_name}". Valid expressions: '
                    f'{", ".join(valid_lookups.keys())}'
                )
            # "contains" behaves differently on JSONFields as it does on other fields.
            # That's why we annotate the queryset with the value.
            # Some discussion about it can be found here:
            # https://code.djangoproject.com/ticket/26511
            cast_to = self.field_type_by_lookup_expr.get(lookup_expr, TextField)
            qs = qs.annotate(
                field_val=Cast(
                    KeyTextTransform(expr["key"], self.field_name),
                    output_field=cast_to(),
                )
            )
            lookup = {f"field_val__{lookup_expr}": Value(expr["value"])}

            qs = qs.filter(**lookup)
        return qs

    def _valid_lookups(self, qs):
        # We need some traversal magic in case field name is a related lookup
        traversals = self.field_name.split("__")
        actual_field = traversals.pop()

        model = qs.model
        for field in traversals:
            model = model._meta.get_field(field).related_model

        return model._meta.get_field(actual_field).get_lookups()


class ActiveGroupFilter(CharFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        if value not in self.parent.request.user.groups:
            raise ValidationError(
                f"Active group '{value}' is not part of user's assigned groups"
            )
        return qs


class TagsFilter(BaseInFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        # Documents must have all given tags
        # including each tag's synonyms
        for tag in value:
            synonyms = models.Tag.objects.filter(
                Q(id=tag) | Q(tag_synonym_group__tags__id=tag)
            )
            qs = qs.filter(tags__in=synonyms)
        return qs


class CategoriesFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        exclude_children = self.parent.request.query_params.get(
            "filter[exclude_children]", False
        )
        filters = Q()

        for category in value.split(","):
            filters |= Q(**{f"{self.field_name}_id": category})
            if not exclude_children:
                filters |= Q(**{f"{self.field_name}__parent__slug": category})

        return qs.filter(filters)


class CategoryFilterSet(FilterSet):
    metainfo = JSONValueFilter(field_name="metainfo")
    active_group = ActiveGroupFilter()
    has_parent = BooleanFilter(field_name="parent", lookup_expr="isnull", exclude=True)
    slug = CharFilter()
    slugs = CharInFilter(field_name="slug", lookup_expr="in")

    class Meta:
        model = models.Category
        fields = ["active_group", "metainfo", "has_parent", "slug", "slugs"]


class DocumentFilterSet(FilterSet):
    metainfo = JSONValueFilter(field_name="metainfo")
    active_group = ActiveGroupFilter()
    tags = TagsFilter()
    marks = CharInFilter()
    category = CategoriesFilter()
    categories = CategoriesFilter(field_name="category")
    # exclude_children is applied in CategoriesFilter, this is needed for DjangoFilterBackend
    exclude_children = BooleanFilter(field_name="title", method=lambda qs, __, ___: qs)

    class Meta:
        model = models.Document
        fields = ["metainfo", "tags"]


class FileFilterSet(FilterSet):
    metainfo = JSONValueFilter(field_name="metainfo")
    document_metainfo = JSONValueFilter(field_name="document__metainfo")
    active_group = ActiveGroupFilter()
    files = BaseCSVFilter(field_name="pk", lookup_expr="in")

    class Meta:
        model = models.File
        fields = ["original", "renderings", "variant", "metainfo", "files"]


class FileSearchFilterSet(FileFilterSet):
    query = CharFilter(method="search_files")

    def search_files(self, queryset, name, value):
        search_queries = [
            Q(
                content_vector=SearchQuery(
                    value,
                    config="simple",
                    search_type=settings.ALEXANDRIA_CONTENT_SEARCH_TYPE,
                )
            )
        ]
        for lang, config in settings.ALEXANDRIA_ISO_639_TO_PSQL_SEARCH_CONFIG.items():
            search_queries.append(
                Q(
                    content_vector=SearchQuery(
                        value,
                        config=config,
                        search_type=settings.ALEXANDRIA_CONTENT_SEARCH_TYPE,
                    )
                )
            )

        search_query = reduce(or_, search_queries)

        latest_files = models.File.objects.filter(
            document=OuterRef("document_id"), variant=models.File.Variant.ORIGINAL
        ).order_by("-created_at")
        queryset = queryset.filter(pk=Subquery(latest_files.values("pk")[:1])).filter(
            search_query
        )

        return queryset

    class Meta:
        model = models.File
        fields = ["original", "renderings", "variant", "metainfo", "files", "query"]


class TagFilterSet(FilterSet):
    metainfo = JSONValueFilter(field_name="metainfo")
    active_group = ActiveGroupFilter()
    with_documents_in_category = CategoriesFilter(field_name="documents__category")
    with_documents_metainfo = JSONValueFilter(field_name="documents__metainfo")
    name = CharFilter(lookup_expr="istartswith")
    name_exact = CharFilter(field_name="name", lookup_expr="iexact")
    # exclude_children is applied in CategoriesFilter, this is needed for DjangoFilterBackend
    exclude_children = BooleanFilter(field_name="name", method=lambda qs, __, ___: qs)

    class Meta:
        model = models.Tag
        fields = [
            "created_by_user",
            "created_by_group",
            "modified_by_user",
            "modified_by_group",
        ]


class MarkFilterSet(FilterSet):
    metainfo = JSONValueFilter(field_name="metainfo")
    active_group = ActiveGroupFilter()
    with_documents_in_category = CharFilter(field_name="documents__category__slug")
    with_documents_metainfo = JSONValueFilter(field_name="documents__metainfo")
    name = CharFilter(lookup_expr="istartswith")

    class Meta:
        model = models.Mark
        fields = [
            "metainfo",
            "active_group",
            "with_documents_in_category",
            "with_documents_metainfo",
            "name",
        ]

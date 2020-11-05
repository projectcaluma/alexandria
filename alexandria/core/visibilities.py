import inspect

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured

from . import models
from .collections import list_duplicates


def filter_queryset_for(model):
    """Decorate function to define filtering of queryset of specific model."""

    def decorate(fn):
        if not hasattr(fn, "_visibilities"):
            fn._visibilities = []

        fn._visibilities.append(model)
        return fn

    return decorate


class BaseVisibility(object):
    """Basic visibility classes to be extended by any visibility implementation.

    In combination with the decorator `@filter_queryset_for` a custom visibility class
    can define filtering on basis of models.

    A custom visibility class could look like this:
    ```
    >>> from alexandria.core.visibilities import BaseVisibility
    ... from alexandria.core.models import BaseModel, Document, File
    ...
    ...
    ... class CustomVisibility(BaseVisibility):
    ...     @filter_queryset_for(BaseModel)
    ...     def filter_queryset_for_all(self, queryset, request):
    ...         return queryset.filter(created_by_user=request.user.username)
    ...
    ...     @filter_queryset_for(Document)
    ...     def filter_queryset_for_document(self, queryset, request):
    ...         return queryset.exclude(category__slug='protected-category')
    ...
    ...     @filter_queryset_for(File)
    ...     def filter_queryset_for_file(self, queryset, request):
    ...         # Limitations for `Document` should also be enforced on `File`.
    ...         return queryset.exclude(document__category__slug='protected-category')
    """

    def __init__(self):
        queryset_fns = inspect.getmembers(self, lambda m: hasattr(m, "_visibilities"))
        queryset_nodes = [
            node.__name__ for _, fn in queryset_fns for node in fn._visibilities
        ]
        queryset_nodes_dups = list_duplicates(queryset_nodes)
        if queryset_nodes_dups:
            raise ImproperlyConfigured(
                f"`filter_queryset_for` defined multiple times for "
                f"{', '.join(queryset_nodes_dups)} in {str(self)}"
            )
        self._filter_querysets_for = {
            node: fn for _, fn in queryset_fns for node in fn._visibilities
        }

    def filter_queryset(self, model, queryset, request):
        for cls in model.mro():
            if cls in self._filter_querysets_for:
                return self._filter_querysets_for[cls](queryset, request)

        return queryset


class Any(BaseVisibility):
    """No restrictions, all models are exposed."""

    pass


class OwnAndAdmin(BaseVisibility):
    """
    Only show own documents and files, except for the admin user.

    This Visibility class filters the queryset, so users only can see their own
    documents and files. For this the `created_by_user` filed is used.

    A user with the username defined in `ADMIN_USERNAME` will be able to see all the
    records.

    This class does not filter Categories and Tags.
    """

    @staticmethod
    def generic_own_and_admin(request, queryset, filters=None, none=False):
        if isinstance(request.user, AnonymousUser):
            return queryset.none()
        elif request.user.username == settings.ADMIN_USERNAME:
            return queryset
        return queryset.filter(**filters)

    @filter_queryset_for(models.Document)
    def filter_queryset_for_document(self, queryset, request):
        return self.generic_own_and_admin(
            request, queryset, {"created_by_user": request.user.username}
        )

    @filter_queryset_for(models.File)
    def filter_queryset_for_file(self, queryset, request):
        return self.generic_own_and_admin(
            request, queryset, {"document__created_by_user": request.user.username}
        )


class Union(BaseVisibility):
    """Union result of a list of configured visibility classes."""

    visibility_classes = []

    def filter_queryset(self, model, queryset, request):
        result_queryset = None
        for visibility_class in self.visibility_classes:
            class_result = visibility_class().filter_queryset(model, queryset, request)
            if result_queryset is None:
                result_queryset = class_result
            else:
                result_queryset = result_queryset.union(class_result)

        if result_queryset is not None:
            queryset = queryset.filter(pk__in=result_queryset.values("pk"))

        return queryset


class Authenticated(BaseVisibility):
    """
    Visibility for authenticated users.

    This is useful if you only ever want to show data
    to authenticated users.

    If you want to make an exception, you can subclass this
    and implement the corresponding filter.
    """

    @filter_queryset_for(models.BaseModel)
    def filter_for_authenticated(self, queryset, request):
        return queryset.none() if isinstance(request.user, AnonymousUser) else queryset

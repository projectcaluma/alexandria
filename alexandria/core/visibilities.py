from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from generic_permissions.visibilities import filter_queryset_for

from . import models


class OwnAndAdmin:
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

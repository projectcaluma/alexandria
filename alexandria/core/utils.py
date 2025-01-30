from django.conf import settings
from django.utils.module_loading import import_string


def get_user_and_group_from_request(request):
    """Return a 2-tuple of `user`, `group` from the given request."""
    getter_fn = import_string(settings.ALEXANDRIA_GET_USER_AND_GROUP_FUNCTION)
    return getter_fn(request)

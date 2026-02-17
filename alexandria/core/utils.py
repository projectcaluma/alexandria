from django.conf import settings
from django.utils.module_loading import import_string
from pathvalidate import sanitize_filename as pathvalidate_sanitize_filename


def get_user_and_group_from_request(request):
    """Return a 2-tuple of `user`, `group` from the given request."""
    getter_fn = import_string(settings.ALEXANDRIA_GET_USER_AND_GROUP_FUNCTION)
    return getter_fn(request)


def sanitize_filename(filename):
    """Use the `pathvalidate` library to sanitize a filename.

    Additionally remove some extra characters.
    """
    # first sanitize using the pathvalidate library.
    filename = pathvalidate_sanitize_filename(filename)

    # remove extra characters that were not removed
    # e.g. the slash is not removed when it is used as a directory separator.
    # we also replace spaces and asterisks with underscores.
    for char in ["/", "*", " "]:
        filename = filename.replace(char, "_")

    # sanitize the result filename again to make sure the
    # modified version is still safe.
    return pathvalidate_sanitize_filename(filename)

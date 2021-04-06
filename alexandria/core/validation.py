import weakref

from django.core.exceptions import ImproperlyConfigured


def validator_for(model_cls):
    def decorator(func):
        if hasattr(func, "_validate_model"):
            raise ImproperlyConfigured(
                f"Method {func.__name__} is already registered to validate {model_cls.__name__}"
            )
        func._validate_model = model_cls
        return func

    return decorator


class BaseValidator:
    """Validate incoming data.

    The validation methods you define here are called at the `validate()` stage
    of the Rest Framework serializer. You can register any method function in your
    validator. Methods starting with underscore `_` will be ignored.

    The validation methods will receive a dict with the incoming data,
    and are expected to return said data. If the data is deemed invalid,
    the method should raise a `ValidationError`.

    Your validator class must inherit from `BaseValidator`. This enables you to
    access the serializer via `self.serializer`, allowing you to look at the request
    object itself, for example.

    Here's a fully functional example:

    ```python
    class MyCustomFileValidator(BaseValidator):
        @validate_for(models.File)
        def validate_file(self, data):
            # do some checks
            return data
    ```

    Note that you must not call `self.serializer.is_valid()` or `self.serializer.validate()`
    from these classes - this will return in an infinite loop.
    """

    def __init__(self, serializer):
        # Weakref to serializer, because we'll have a reference circle
        # otherwise (serializer -> validator -> serializer...), preventing
        # garbage collection
        self.serializer = weakref.proxy(serializer)

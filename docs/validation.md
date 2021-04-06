# Custom validation

Alexandria allows you to define custom validations. To use this, create a new
file, ensure it's mounted into the container, and set the env variable `VALIDATION_CLASSES`
to the classes you want to load.

A validation class can then define methods that are called to validate incoming
data. The calling convention is  similar to those of the Django Rest Framework
serializers: The incoming data is passed as a dict, which may be inspected and
modified. The validated data is then returned for further processing.
If the data is deemed invalid, the method shouldd raise a `ValidationError`.

You can also access the serializer, the context (including the raw request) via
`self.serializer`.

To implement a custom validator, you need to create a class, inherit from `BaseValidator`,
then define some validation methods within it. The validation methods need to be
decorated using `@validator_for(model_class_name)`.

Here's a fully functional example:

```python
from alexandria.core.validation import BaseValidator, validator_for
from alexandria.core import models

class MyCustomFileValidator(BaseValidator):
    @validator_for(models.File)
    def validate(self, data):
        # do some checks
        return data
```

Note that you must not call `self.serializer.is_valid()` or `self.serializer.validate()`
from these classes - this will return in an infinite loop.

Validators may be stacked! Which means you can define multiple validators
for the same model, and they will be called one after the other. However,
the same validator method may not be used for multiple models.

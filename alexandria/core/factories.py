from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from . import models


class BaseFactory(DjangoModelFactory):
    created_by_user = "admin"
    created_by_group = "admin"
    modified_by_user = "admin"
    modified_by_group = "admin"

    class Meta:
        abstract = True


class CategoryFactory(BaseFactory):
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text")
    color = Faker("color")
    meta = {}

    class Meta:
        model = models.Category


class TagFactory(BaseFactory):
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Tag


class DocumentFactory(BaseFactory):
    title = Faker("name")
    description = Faker("text")
    category = SubFactory(CategoryFactory)

    class Meta:
        model = models.Document


class FileFactory(BaseFactory):
    name = Faker("name")
    document = SubFactory(DocumentFactory)

    class Meta:
        model = models.File


class DocumentTagsFactory(DjangoModelFactory):
    document = SubFactory(DocumentFactory)
    tag = SubFactory(TagFactory)

    class Meta:
        model = models.Document.tags.through

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from . import models


class CategoryFactory(DjangoModelFactory):
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Category


class TagFactory(DjangoModelFactory):
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Tag


class DocumentFactory(DjangoModelFactory):
    name = Faker("name")
    title = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Document


class DocumentTagsFactory(DjangoModelFactory):
    document = SubFactory(DocumentFactory)
    tag = SubFactory(TagFactory)

    class Meta:
        model = models.Document.tags.through

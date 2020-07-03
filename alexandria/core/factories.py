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
    title = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Document


class FileFactory(DjangoModelFactory):
    name = Faker("name")
    document = SubFactory(DocumentFactory)

    class Meta:
        model = models.File


class DocumentTagsFactory(DjangoModelFactory):
    document = SubFactory(DocumentFactory)
    tag = SubFactory(TagFactory)

    class Meta:
        model = models.Document.tags.through

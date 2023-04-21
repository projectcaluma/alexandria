from factory import Faker, SubFactory, post_generation
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
    metainfo = {}

    class Meta:
        model = models.Category


class TagFactory(BaseFactory):
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Tag


class TagSynonymGroupFactory(BaseFactory):
    class Meta:
        model = models.TagSynonymGroup

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)


class DocumentFactory(BaseFactory):
    class Meta:
        model = models.Document

    title = Faker("name")
    description = Faker("text")
    category = SubFactory(CategoryFactory)

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)


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

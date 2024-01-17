import factory
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from alexandria.core.tests import file_data

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


class TagSynonymGroupFactory(BaseFactory):
    class Meta:
        model = models.TagSynonymGroup

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:  # pragma: todo cover
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)


class TagFactory(BaseFactory):
    name = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Tag


class MarkFactory(BaseFactory):
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Mark


class DocumentFactory(BaseFactory):
    class Meta:
        model = models.Document

    title = Faker("name")
    description = Faker("text")
    category = SubFactory(CategoryFactory)
    date = Faker("date")

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:  # pragma: todo cover
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)

    @post_generation
    def marks(self, create, extracted, **kwargs):  # pragma: todo cover
        if not create:
            return

        if extracted:
            for mark in extracted:
                self.marks.add(mark)


class FileFactory(BaseFactory):
    """Factory for File.

    Usage:
    If you want a nice set of Document, File with thumbnails:

    `thumb = FileFactory(variant=File.Variant.THUMBNAIL)`

    for multiple versions:
    `thumb_v2 = FileFactory(variant=File.Variant.THUMBNAIL, document=thumb.document)`


    """

    name = factory.Maybe(
        factory.LazyAttribute(lambda o: o.variant == models.File.Variant.ORIGINAL),
        yes_declaration=Faker("name"),
        no_declaration=factory.LazyAttribute(
            lambda o: f"{o.original.name}_preview.jpg"
        ),
    )
    document = SubFactory(DocumentFactory)
    variant = models.File.Variant.ORIGINAL
    content = factory.Maybe(
        factory.LazyAttribute(lambda o: o.variant == models.File.Variant.THUMBNAIL),
        yes_declaration=factory.django.ImageField(
            filename="thumb_preview.jpg", width=256, height=256, format="JPEG"
        ),
        no_declaration=factory.django.FileField(
            filename="the_file.png", data=file_data.png
        ),
    )
    original = factory.Maybe(
        factory.LazyAttribute(lambda o: o.variant == models.File.Variant.THUMBNAIL),
        SubFactory(
            "alexandria.core.factories.FileFactory",
            variant=models.File.Variant.ORIGINAL,
            document=factory.SelfAttribute("..document"),
        ),
    )

    class Meta:
        model = models.File


class DocumentTagsFactory(DjangoModelFactory):
    document = SubFactory(DocumentFactory)
    tag = SubFactory(TagFactory)

    class Meta:
        model = models.Document.tags.through


class DocumentMarksFactory(DjangoModelFactory):
    document = SubFactory(DocumentFactory)
    mark = SubFactory(MarkFactory)

    class Meta:
        model = models.Document.marks.through

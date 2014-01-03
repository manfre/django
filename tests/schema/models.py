from django.core.apps.cache import AppCache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Because we want to test creation and deletion of these as separate things,
# these models are all inserted into a separate AppCache so the main test
# runner doesn't migrate them.

new_app_cache = AppCache()


class Author(models.Model):
    name = models.CharField(max_length=255)
    height = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        app_cache = new_app_cache


class AuthorWithM2M(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_cache = new_app_cache


class Book(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=100, db_index=True)
    pub_date = models.DateTimeField()
    # tags = models.ManyToManyField("Tag", related_name="books")

    class Meta:
        app_cache = new_app_cache


class BookWithM2M(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=100, db_index=True)
    pub_date = models.DateTimeField()
    tags = models.ManyToManyField("TagM2MTest", related_name="books")

    class Meta:
        app_cache = new_app_cache


class BookWithSlug(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=100, db_index=True)
    pub_date = models.DateTimeField()
    slug = models.CharField(max_length=20, unique=True)

    class Meta:
        app_cache = new_app_cache
        db_table = "schema_book"


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        app_cache = new_app_cache


class TagM2MTest(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        app_cache = new_app_cache


class TagIndexed(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        app_cache = new_app_cache
        index_together = [["slug", "title"]]


class TagUniqueRename(models.Model):
    title = models.CharField(max_length=255)
    slug2 = models.SlugField(unique=True)

    class Meta:
        app_cache = new_app_cache
        db_table = "schema_tag"


class UniqueTest(models.Model):
    year = models.IntegerField()
    slug = models.SlugField(unique=False)

    class Meta:
        app_cache = new_app_cache
        unique_together = ["year", "slug"]


class BookWithLongName(models.Model):
    author_foreign_key_with_really_long_field_name = models.ForeignKey(Author)

    class Meta:
        app_cache = new_app_cache

# Copied form tests/reserved_names/models.py
@python_2_unicode_compatible
class Thing(models.Model):
    when = models.CharField(max_length=1, primary_key=True)
    join = models.CharField(max_length=1)
    like = models.CharField(max_length=1)
    drop = models.CharField(max_length=1)
    alter = models.CharField(max_length=1)
    having = models.CharField(max_length=1)
    where = models.DateField(max_length=1)
    has_hyphen = models.CharField(max_length=1, db_column='has-hyphen')

    class Meta:
        app_cache = new_app_cache
        db_table = 'select'

    def __str__(self):
        return self.when

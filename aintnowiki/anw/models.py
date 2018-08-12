import random
import shlex

from django.db import models
from django.urls import reverse
import tinymce.models
import tagging.fields


class PageManager(models.Manager):
    def random(self, howmany=1):
        pks = set()
        count = self.count()
        limit = min(
            howmany,
            count
        )

        while True:
            try:
                random_page = self.model.objects.get(pk = random.randint(0, count - 1))
            except self.model.DoesNotExist:
                continue
            else:
                pks.add(random_page)
                if len(pks) >= limit:
                    break

        return pks


# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, help_text='Timestamp - created')
    changed = models.DateTimeField(auto_now=True, help_text='Timestamp - last changed')
    title = models.CharField(max_length=75, help_text='Title of the Page')
    slug = models.SlugField(help_text='Slug used in URL', blank=False, unique=True)
    featured = models.BooleanField(help_text='Should it appear on the navigation bar?', blank=True, default=False)
    footer = models.BooleanField(help_text='Should it appear in the footer?', blank=True, default=False)
    tags = tagging.fields.TagField(help_text='List of Tags')
    meta_keywords = models.TextField(help_text="Keywords for meta tag.", blank=True, null=True)
    meta_description = models.TextField(help_text="Description for meta tag and children listing.", blank=True, null=True)

    class Meta:
        abstract=True

    def __str__(self):
        return self.title

    def get_tags(self):
        return tagging.models.Tag.objects.get_for_object(self)

    def get_keywords(self):
        tags = map(lambda x: str(x), self.get_tags())
        keywords = shlex.split(self.meta_keywords)
        return ', '.join(list(tags) + keywords)


class Page(BaseModel):
    objects = PageManager()
    body = tinymce.models.HTMLField(help_text='Content of the Page')
    parent = models.ForeignKey('Page', models.PROTECT, help_text='Parent Page', blank=True, null=True, related_name='children_set')

    def get_breadcrumbs(self):
        crumbs = []
        if self.parent:
            crumbs += self.parent.get_breadcrumbs()
        crumbs.append(self)
        return crumbs

    def get_children(self):
        return self.children_set.all()

    def get_url(self):
        return reverse("anw-page", args=(self.slug,))


class Image(BaseModel):
    body = models.ImageField(upload_to='uploads/%Y/%m/%d/')

    def get_url(self):
        return "#"
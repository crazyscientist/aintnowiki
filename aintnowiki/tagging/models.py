from json import dumps

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from rest_framework import serializers


class Tag(models.Model):
    name = models.CharField(max_length=64, help_text="Verbose name", unique=True)
    slug = models.SlugField(max_length=64, help_text="Unique URL identifier", unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               help_text="Generic parent tag")
    description = models.CharField(max_length=255, help_text="Short description", blank=True)
    attributes = models.JSONField(help_text="Additional HTML attributes", null=True, blank=True)

    def __str__(self):
        return self.name

    def as_json(self):
        return dumps({field.name: field.value_from_object(self)
                      for field in self._meta.fields
                      if field.name != "parent"})

    class Meta:
        ordering = ('name',)


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField(db_index=True)
    object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "{}:{}".format(self.object, self.tag)

    class Meta:
        ordering = ('tag', 'content_type', 'object_id')
        unique_together = ('tag', 'content_type', 'object_id')


class BasicTagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    slug = serializers.SlugField()
    name = serializers.CharField()


class TagSerializer(BasicTagSerializer):
    parent = serializers.IntegerField(source="parent_id")
    description = serializers.CharField()
    attributes = serializers.JSONField()

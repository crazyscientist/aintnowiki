from django.db import models
from django.urls import reverse
from rest_framework import serializers

from tagging.mixins import TaggedMixin
from tagging.models import BasicTagSerializer
from .widgets import ToastUIField


class Page(TaggedMixin):
    title = models.CharField(max_length=255, help_text="Page title")
    slug = models.SlugField(max_length=255, unique=True, help_text="Unique URL identifier")
    created = models.DateTimeField(auto_now_add=True, help_text="Creation date")
    changed = models.DateTimeField(auto_now=True, help_text="Last change")
    summary = models.TextField(help_text="Short summary to show in listing")
    content = ToastUIField(help_text="Page content")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-changed',)


class BasePageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    summary = serializers.CharField()
    changed = serializers.DateTimeField()
    tags = BasicTagSerializer(many=True, source="get_tags")
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('wiki:page-detail', kwargs={"slug": obj.slug})


class PageListSerializer(BasePageSerializer):
    apiurl = serializers.SerializerMethodField()

    def get_apiurl(self, obj):
        return reverse('api_wiki:page', kwargs={"pk": obj.pk})


class PageDetailSerializer(BasePageSerializer):
    created = serializers.DateTimeField()
    content = serializers.CharField()

from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Model

from .models import TaggedItem


class TaggedMixin(Model):
    tags = GenericRelation(TaggedItem)

    def get_tags(self):
        if "tags" in getattr(self, "_prefetched_objects_cache", {}):
            return (t.tag for t in self.tags.all())

        return (t.tag for t in self.tags.all().select_related("tag"))

    def display_tags(self):
        return ", ".join(tag.name for tag in self.get_tags())

    class Meta:
        abstract = True

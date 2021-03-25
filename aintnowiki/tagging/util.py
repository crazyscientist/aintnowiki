from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model

from .models import Tag, TaggedItem, TagSerializer


def get_tag_tree(model=None, serialize=False):
    """
    Get hierarchical tag tree
    """
    def get_children(tag, tags):
        return [to_leaf(child, tags) for child in tags.values() if child.parent_id == tag.id]

    def to_leaf(tag, tags):
        tag_data = TagSerializer(tag).data if serialize else tag
        return {"tag": tag_data, "children": get_children(tag, tags)}

    cache_key = "tag:tree:{}".format(model._meta.model_name if model is not None else "all")
    tree = cache.get(cache_key)
    if tree:
        return tree

    qs = Tag.objects.all().order_by("parent_id", "name")
    if model:
        content_type = ContentType.objects.get_for_model(model)
        qs = qs.filter(id__in=TaggedItem.objects.filter(content_type=content_type).values("tag_id"))

    tags = {x.id: x for x in qs}
    tree = [to_leaf(tag, tags)
            for tag in tags.values()
            if tag.parent_id is None or tag.parent_id not in tags]
    cache.set(cache_key, tree)

    return tree


class FancyJsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return {field.name: field.value_from_object(o) for field in o._meta.fields}

        return super().default(o)

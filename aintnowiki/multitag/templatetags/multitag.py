import re

from django.template import Node, Library
from django.db.models import Count

from tagging.models import Tag
from tagging.utils import calculate_cloud, LOGARITHMIC


register = Library()


class TagCloud(Node):
    def __init__(self, context_var, **kwargs):
        self.context_var = context_var
        self.kwargs = kwargs

    def render(self, context):
        tags = Tag.objects.annotate(count = Count("items")).exclude(count = 0)
        context[self.context_var] = calculate_cloud(tags, **self.kwargs)
        return ''


@register.tag()
def get_tagcloud(parser, token):
    bits = token.contents.split()
    print("= DEBUG =", bits)
    kwargs = {}
    context_var = "tagcloud"

    try:
        as_index = bits.index("as")
    except ValueError:
        pass
    else:
        context_var = bits[as_index + 1]

    pattern = re.compile("(?P<key>[^= ]+)=(?P<value>[^ =]+)")
    for bit in bits:
        match = pattern.match(bit)
        if match:
            kwargs[match.group("key")] = match.group("value")

    if "steps" in kwargs:
        kwargs["steps"] = int(kwargs["steps"])
    print("= DEBUG = KWARGS", kwargs)
    return TagCloud(context_var, **kwargs)

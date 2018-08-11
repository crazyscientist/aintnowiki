import re

from django.template import Node, Library, TemplateSyntaxError
from django.db.models import Count

from tagging.models import Tag
from tagging.utils import calculate_cloud, LOGARITHMIC, LINEAR


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
        try:
            kwargs["steps"] = int(kwargs["steps"])
        except:
            raise TemplateSyntaxError("'steps' needs to be a positive integer.")
    if "distribution" in kwargs:
        try:
            kwargs["distribution"] = int(kwargs["distribution"])
        except:
            raise TemplateSyntaxError(
                "'distribution' needs to be one of: tagging.utils.LINEAR or tagging.utils.LOGARITHMIC"
            )
        else:
            if kwargs["distribution"] not in [LINEAR, LOGARITHMIC]:
                raise TemplateSyntaxError(
                "'distribution' needs to be one of: tagging.utils.LINEAR or tagging.utils.LOGARITHMIC"
            )
    return TagCloud(context_var, **kwargs)

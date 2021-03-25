from django import template

from ..util import get_tag_tree


register = template.Library()


@register.inclusion_tag("tag_nav.html")
def tag_nav(model):
    tree = get_tag_tree(model)

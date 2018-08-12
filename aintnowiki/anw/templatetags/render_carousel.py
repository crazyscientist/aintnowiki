from django import template

import anw.models


register = template.Library()


@register.inclusion_tag('object_list/object_carousel.html')
def render_carousel(title, objects):
    return {
        "carousel_title": title,
        "carousel": objects
    }

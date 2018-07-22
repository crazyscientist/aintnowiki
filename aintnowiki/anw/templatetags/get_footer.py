from django import template

import anw.models


register = template.Library()


@register.simple_tag()
def get_footer_items():
    pages = anw.models.Page.objects.filter(footer=True).order_by("title")

    return pages

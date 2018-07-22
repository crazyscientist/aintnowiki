from django import template

import anw.models


register = template.Library()


@register.simple_tag()
def get_navigation_tree():
    all = anw.models.Page.objects.filter(featured = True).order_by("title")
    nav = list(all.filter(parent = None))
    for item in all.exclude(parent = None):
        parent = item.parent
        while parent.parent is not None:
            parent = parent.parent
        for i in range(len(nav)):
            if nav[i].slug != parent.slug:
                continue
            if not hasattr(nav[i], "children"):
                nav[i].children = []
            nav[i].children.append(item)
            break
        else:
            parent.children = [item]
            nav.append(parent)

    return nav
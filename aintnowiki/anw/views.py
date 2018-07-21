import random
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.conf import settings

from tagging.models import Tag

import anw.models
import time


# Create your views here.
class PageView(DetailView):
    template_name = "page.html"
    model = anw.models.Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["navigation"] = self.get_navigation_tree()
        context["footer"] = anw.models.Page.objects.filter(footer=True).order_by("title")
        context["tags"] = Tag.objects.get_for_object(self.get_object())
        return context

    @staticmethod
    def get_navigation_tree():
        all = anw.models.Page.objects.filter(featured=True).order_by("title")
        nav = list(all.filter(parent=None))
        for item in all.exclude(parent=None):
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


class HomeView(PageView):
    template_name="page.html"
    model = anw.models.Page
    queryset = model.objects.filter(slug=getattr(settings, "ANW_HOMEPAGE", "home"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["tags"] = True
        pks = set()
        count = self.model.objects.count()
        while len(pks) < 5 or len(pks) < count - 1:
            pks.add(random.randint(0, count-1))
        context["carousel"] = self.model.objects.filter(pk__in=pks)

        return context
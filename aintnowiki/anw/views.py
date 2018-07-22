import random
from django.views.generic import DetailView
from django.conf import settings

import anw.models


# Create your views here.
class PageView(DetailView):
    template_name = "page.html"
    model = anw.models.Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HomeView(PageView):
    template_name="index.html"
    model = anw.models.Page
    queryset = model.objects.filter(slug=getattr(settings, "ANW_HOMEPAGE", "home"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["tags"] = True
        pks = set()
        count = self.model.objects.count()
        limit = min(
            getattr(settings, "ANW_NUM_CARDS", 5),
            count
        )
        while True:
            pks.add(random.randint(1, count-1))
            if len(pks) >= limit:
                break
        context["carousel"] = self.model.objects.filter(pk__in=pks)

        return context
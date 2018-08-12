from django.db.models import Count, Q
from django.http import Http404
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import FormMixin
from django.conf import settings

import anw.forms
from anw.mixins import JSONResponseMixin
from anw.models import Page, Image


class FakeQuerySet(object):
    model=[]


# Create your views here.
class PageView(DetailView):
    template_name = "page.html"
    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel"] = context["object"].get_children()
        return context


class HomeView(PageView):
    template_name = "index.html"
    model = Page
    queryset = model.objects.filter(slug=getattr(settings, "ANW_HOMEPAGE", "home"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["tags"] = True

        context["random_carousel"] = self.model.objects.random(
            getattr(settings, "ANW_NUM_CARDS", 5)
        )
        return context


class SearchView(FormMixin, ListView):
    form_class = anw.forms.SearchForm
    model = Page
    template_name = "object_list.html"
    ordering = "slug"
    paginate_by = 16

    def get_queryset(self):
        self._my_form = self.form_class(getattr(self.request, self.request.method, {}))
        if not self._my_form.is_valid() or self._my_form.cleaned_data.get("searchstring", None) in [None, ""]:
            return self.model.objects.none()

        return self.model.objects.filter(
            Q(title__icontains=self._my_form.cleaned_data["searchstring"])|
            Q(body__icontains=self._my_form.cleaned_data["searchstring"])|
            Q(tags__icontains=self._my_form.cleaned_data["searchstring"])|
            Q(meta_keywords__icontains=self._my_form.cleaned_data["searchstring"])|
            Q(meta_description__icontains=self._my_form.cleaned_data["searchstring"])
        ).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = getattr(self, "_my_form", None)
        return context

    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response(context, **response_kwargs)


class SitemapView(TemplateView):
    template_name = "sitemap.html"


class SitemapJsonView(JSONResponseMixin, ListView):
    # queryset = anw.models.Page.objects
    form_class = anw.forms.SitemapForm
    template_name = "object_list.html"

    @staticmethod
    def object_to_jstree_json(obj):
        return {
            "id": obj.slug,
            # "parent": getattr(obj.parent, "slug", "#") or "#",
            "text": obj.title,
            "children": bool(obj.num_children),
            "a_attr": {"href": obj.get_url()}
        }

    def get_data(self, context):
        return [self.object_to_jstree_json(x)for x in context.get("object_list", [])]

    def get_queryset(self):
        form = self.form_class(getattr(self.request, self.request.method, {}))
        if not form.is_valid():
            raise Http404("Invalid input parameters")

        parent = form.cleaned_data.get("slug", None)
        if parent in [None, ""]:
            queryset = anw.models.Page.objects.filter(parent=None)
        else:
            queryset = anw.models.Page.objects.filter(parent__slug=parent)

        return queryset.annotate(num_children=Count('children_set'))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)


class ImageListView(ListView):
    model = Image
    template_name = "object_list.html"
    ordering = "slug"
    paginate_by = 16

    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response(context, **response_kwargs)

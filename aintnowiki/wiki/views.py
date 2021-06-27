from pathlib import Path
from urllib.parse import urljoin
from uuid import uuid1

from django.conf import settings as gsettings
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q, Count, Value
from django.forms import Form, ImageField
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView, DetailView, FormView, View, ListView
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from tagging.util import get_tag_tree
from .models import Page, PageListSerializer, PageDetailSerializer
from . import settings


class TagTreeView(APIView):
    def get(self, request, format=None):
        return Response(get_tag_tree(serialize=True))


class ApiListView(ListAPIView):
    queryset = Page.objects.all().prefetch_related("tags", "tags__tag")
    serializer_class = PageListSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-changed']

    def filter_queryset(self, queryset):
        tags = self.request.query_params.getlist("tag", [])
        search_string = self.request.query_params.get("q", None)

        if not tags and not search_string:
            return queryset

        if search_string:
            queryset = queryset.filter(Q(title__icontains=search_string) |
                                       Q(summary__icontains=search_string))

        if tags:
            q = Q()
            for tag in tags:
                if isinstance(tag, int) or tag.isdigit():
                    q |= Q(tags__tag_id=tag)
                else:
                    q |= Q(tags__tag__slug=tag)

            queryset = queryset\
                .filter(q)\
                .annotate(numtags=Count("tags__tag_id", distinct=True))\
                .filter(numtags=len(tags))

        return queryset


class ApiPageView(RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer


class WikiMixin:
    template_name = "wiki.html"
    model = Page
    disallow_indexing = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["BRAND_HTML"] = settings.BRAND_HTML
        context["PLANTUML_RENDERER_URL"] = settings.PLANTUML_RENDERER_URL
        context["navigation"] = get_tag_tree(serialize=True)
        context["noindex"] = self.disallow_indexing

        return context


class VueView(WikiMixin, TemplateView):
    disallow_indexing = True


class PageView(WikiMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["json_object"] = PageDetailSerializer(context["object"]).data

        return context


class ImageUploadForm(Form):
    image = ImageField()


class AdminImageUploadView(FormView):
    form_class = ImageUploadForm
    template_name = "admin_wiki_img_upload.html"
    media_rel_path = Path("uploads/uuid/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Upload Image"
        return context

    @property
    def media_dir(self):
        target_dir = gsettings.MEDIA_ROOT.joinpath(self.media_rel_path)
        if not target_dir.is_dir():
            target_dir.mkdir(parents=True, exist_ok=True)

        return target_dir

    def get_media_url(self, path):
        rel_path = path.relative_to(gsettings.MEDIA_ROOT)
        return urljoin(gsettings.MEDIA_URL, rel_path.as_posix())

    def form_valid(self, form):
        file_ext = Path(form.cleaned_data["image"].name).suffix
        target_file = self.media_dir.joinpath(Path(uuid1().hex + file_ext))
        with target_file.open("wb") as f:
            for chunk in form.cleaned_data["image"]:
                f.write(chunk)

        return JsonResponse({
            "status": "created",
            "url": self.get_media_url(target_file)
        })


class FqdnMixin:
    @cached_property
    def fqdn(self):
        return "{}://{}".format(self.request.scheme, self.request.get_host())


class RobotView(FqdnMixin, View):
    def get(self, request, *args, **kwargs):
        sitemap_url = urljoin(self.fqdn, reverse("wiki:sitemap"))
        return HttpResponse("Sitemap: {}".format(sitemap_url))


class SitemapView(FqdnMixin, ListView):
    template_name = "sitemap.xml"

    def get_queryset(self):
        return Page.objects.all().only("slug", "changed").annotate(_fqdn=Value(self.fqdn))


def handler404(request, exception=None, template_name="404.html"):
    path = Path(request.path)
    context = {
        "BRAND_HTML": settings.BRAND_HTML,
        "noindex": True,
        "objects": Page.objects
            .annotate(similarity=TrigramSimilarity('slug', path.name))
            .filter(similarity__gte=0.5)
            .only("title", "slug", "summary")
            .order_by("-similarity")
    }
    return render(request, template_name=template_name, context=context, status=404)

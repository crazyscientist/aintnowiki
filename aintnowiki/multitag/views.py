from django.views.generic import DetailView
from tagging.models import Tag, TaggedItem


# Create your views here.
class TagView(DetailView):
    template_name = "page_list.html"
    model = Tag
    slug_field = "name"
    slug_url_kwarg = "tag"
    context_object_name = "tag"

    related_tags = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = [x.object for x in TaggedItem.objects.filter(tag=self.object)]
        sorted(context["object_list"], key=lambda x: x.slug)
        return context
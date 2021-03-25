from django.contrib.admin import ModelAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.forms import ModelForm

from aintnowiki.admin import custom_admin_site
from tagging.models import TaggedItem
from .models import Page
from .widgets import ToastUIWidget


class TagInline(GenericStackedInline):
    model = TaggedItem


class AdminPageForm(ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'slug', 'summary', 'content')
        widgets = {
            'content': ToastUIWidget
        }


class PageAdmin(ModelAdmin):
    list_display = ('title', 'created', 'changed', 'display_tags')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TagInline]
    form = AdminPageForm


custom_admin_site.register(Page, PageAdmin)

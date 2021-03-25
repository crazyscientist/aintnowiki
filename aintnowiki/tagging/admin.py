from django.contrib import admin

from aintnowiki.admin import custom_admin_site
from .models import Tag, TaggedItem


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ('tag', 'object')
    fields = ('tags',)


custom_admin_site.register(Tag, TagAdmin)
custom_admin_site.register(TaggedItem, TaggedItemAdmin)

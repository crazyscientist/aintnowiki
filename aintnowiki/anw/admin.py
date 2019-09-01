from django.contrib import admin
from anw.models import Page, Image


# Register your models here.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'parent', 'featured')
    list_filter = ('parent', 'featured')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'featured')

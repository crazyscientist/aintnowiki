from django.contrib import admin
import anw.models


# Register your models here.
@admin.register(anw.models.Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'parent', 'featured')
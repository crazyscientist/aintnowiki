from django.contrib import admin
from django.urls import path

from wiki.views import AdminImageUploadView


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('image-upload/', self.admin_view(AdminImageUploadView.as_view()),
                 name="img_upload")
        ]
        return custom_urls + urls


custom_admin_site = CustomAdminSite()

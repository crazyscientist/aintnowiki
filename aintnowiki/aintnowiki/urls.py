"""aintnowiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from wiki.admin import custom_admin_site
from wiki.views import RobotView

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('api/tagging/', include(('tagging.api_urls', 'tagging'), namespace="api_tagging")),
    path('api/wiki/', include(('wiki.api_urls', 'wiki'), namespace="api_wiki")),
    path('wiki/', include(('wiki.urls', 'wiki'), namespace="wiki")),
    path('', RedirectView.as_view(pattern_name='wiki:index', permanent=True)),
    path('robots.txt', RobotView.as_view(), name="robots"),
    re_path(r'^{}(?P<path>.*)$'.format(settings.STATIC_URL.lstrip("/")), serve,
            {"document_root": settings.STATIC_ROOT}),
    re_path(r'^{}(?P<path>.*)$'.format(settings.MEDIA_URL.lstrip("/")), serve,
            {"document_root": settings.MEDIA_ROOT}),
]

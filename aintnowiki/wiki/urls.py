from django.urls import path

from .views import PageView, VueView, SitemapView


urlpatterns = [
    path('', VueView.as_view(), name='index'),
    path('sitemap/', SitemapView.as_view(), name='sitemap'),
    path('<slug:slug>/', PageView.as_view(), name='page-detail'),
]

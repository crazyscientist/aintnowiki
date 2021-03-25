from django.urls import path

from .views import PageView, VueView


urlpatterns = [
    path('', VueView.as_view(), name='index'),
    path('<slug:slug>/', PageView.as_view(), name='page-detail'),
]

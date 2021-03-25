from django.urls import path

from .views import ApiPageView, ApiListView, TagTreeView


urlpatterns = [
    path('tags/', TagTreeView.as_view(), name="tags"),
    path('pages/', ApiListView.as_view(), name="pages"),
    path('pages/<int:pk>/', ApiPageView.as_view(), name="page")
]

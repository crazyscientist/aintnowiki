from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination

from .models import Tag, TagSerializer


class TagPagination(CursorPagination):
    ordering = 'name'


class TagView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = TagPagination


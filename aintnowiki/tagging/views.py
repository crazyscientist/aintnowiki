from rest_framework.generics import ListAPIView

from .models import Tag, TagSerializer


class TagView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

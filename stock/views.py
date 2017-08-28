from rest_framework.generics import ListAPIView, RetrieveAPIView

from stock.models import Item

from .serializers import ItemSerializer

class ItemListAPIView(ListAPIView):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer

class ItemDetailAPIView(ListAPIView):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer

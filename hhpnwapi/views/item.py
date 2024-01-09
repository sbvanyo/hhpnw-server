"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hhpnwapi.models import Item


class ItemView(ViewSet):
    """hhpnw item view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single item.
        Returns: Response -- JSON serialized item"""
        
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all items.
        Returns: Response -- JSON serialized list of items"""
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)




class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items"""
    class Meta:
        model = Item
        fields = ('id', 'name', 'price')

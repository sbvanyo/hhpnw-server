"""View module for handling requests about items"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hhpnwapi.models import OrderItem, Order, Item


class OrderItemView(ViewSet):
    """hhpnw order item view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order item.
        Returns: Response -- JSON serialized order item"""

        order_item = OrderItem.objects.get(pk=pk)
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all order_items.
        Returns: Response -- JSON serialized list of order_items"""
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

class OrderItemSerializer(serializers.ModelSerializer):
    """JSON serializer for order items"""
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'item', 'quantity')
        depth = 1

"""View module for handling requests about items"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hhpnwapi.models import Order, User


class OrderView(ViewSet):
    """hhpnw order view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single order.
        Returns: Response -- JSON serialized order"""

        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all orders.
        Returns: Response -- JSON serialized list of orders"""
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized order instance"""
        user = User.objects.get(uid=request.data["user"])

        order = Order.objects.create(
            user=user,
            name=request.data["name"],
            open=request.data["open"],
            phone=request.data["phone"],
            email=request.data["email"],
            type=request.data["type"],
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)




class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for orders"""
    class Meta:
        model = Order
        fields = ('id', 'user', 'name', 'open', 'phone', 'email', 'type')

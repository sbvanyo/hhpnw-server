"""View module for handling requests about items"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from hhpnwapi.models import Order, User, Item, OrderItem


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


    def update(self, request, pk):
        """Handle PUT requests for an order
        Returns: Response -- Empty body with 204 status code"""

        order = Order.objects.get(pk=pk)
        order.name = request.data["name"]
        order.phone = request.data["phone"]
        order.email = request.data["email"]
        order.type = request.data["type"]
        order.open = request.data["open"]

        order.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for an order
        Returns: Response -- Empty body with 204 status code"""
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



# ADD/REMOVE ORDERITEM

    @action(methods=['post'], detail=True)
    def add_order_item(self, request, pk):
        """Post request for a user to add an item to an order"""

        item = Item.objects.get(pk=request.data["item"])
        order = Order.objects.get(pk=pk)
        orderitem = OrderItem.objects.create(
            item=item,
            order=order
        )
        return Response({'message': 'Item added to order'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove_order_item(self, request, pk):
        """Delete request for a user to remove an item from an order"""

        orderitem = request.data.get("order_item")
        OrderItem.objects.filter(pk=orderitem, order__pk=pk).delete()

        return Response("Order item removed", status=status.HTTP_204_NO_CONTENT)

class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for orders"""
    class Meta:
        model = Order
        fields = ('id', 'user', 'name', 'open', 'phone', 'email', 'type')

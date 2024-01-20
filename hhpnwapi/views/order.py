"""View module for handling requests about items"""
from datetime import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from hhpnwapi.models import Order, User, Item, OrderItem, Revenue
# from order_item import OrderItemSerializer


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

        # Handling order items
        items = request.data.get("items", [])
        for item_data in items:
            item_id = item_data.get("itemId")
            quantity = item_data.get("quantity", 0)
            if item_id is not None and quantity > 0:
                item = Item.objects.get(pk=item_id)
                OrderItem.objects.create(
                    order=order,
                    item=item,
                    quantity=quantity
                )

        serializer = OrderSerializer(order)
        return Response(serializer.data)


    def update(self, request, pk):
        """Handle PUT requests for an order
        Returns: Response -- Empty body with 204 status code"""
        try:
            order = Order.objects.get(pk=pk)

            # Capture the current 'open' status before updating
            is_order_currently_open = order.open

            # Update the order
            order.name = request.data["name"]
            order.phone = request.data["phone"]
            order.email = request.data["email"]
            order.type = request.data["type"]
            order.open = request.data["open"]  # This could be 'False' if closing
            order.save()

            # Check if the order is being closed
            if is_order_currently_open and not order.open:
                # Calculate subtotal, tip, and total
                subtotal = sum(item.quantity * item.item.price for item in OrderItem.objects.filter(order=order))
                tip = request.data.get("tip", 0)
                total = subtotal + tip
                payment = request.data.get("payment", "")

                # Create a revenue node
                Revenue.objects.create(
                    order=order,
                    date=datetime.now(),
                    payment=payment,
                    subtotal=subtotal,
                    tip=tip,
                    total=total
                )

            # Process updated item quantities
            updated_items = request.data.get("items", [])
            existing_items = {item.item.id: item for item in OrderItem.objects.filter(order=order)}

            # Update or delete existing items, and add new items
            for item_data in updated_items:
                item_id = item_data.get("itemId")
                quantity = item_data.get("quantity", 0)

                if item_id in existing_items:
                    # Update the existing item quantity
                    if quantity > 0:
                        existing_items[item_id].quantity = quantity
                        existing_items[item_id].save()

                else:
                    # Add new items
                    if quantity > 0:
                        try:
                            item = Item.objects.get(pk=item_id)
                            OrderItem.objects.create(order=order, item=item, quantity=quantity)
                        except Item.DoesNotExist:
                            # Handle the case where the item does not exist
                            pass

            # Handle items not included in the updated list (set to 0 in frontend but not sent)
            for item_id in existing_items:
                if item_id not in [item.get('itemId') for item in updated_items]:
                    existing_items[item_id].delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        # except Exception as e:
        #     # Log the exception or handle it as appropriate
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        


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
        quantity = request.data.get("quantity", 0)
        order = Order.objects.get(pk=pk)
        orderitem = OrderItem.objects.create(
            item=item,
            order=order,
            quantity=quantity
        )
        return Response({'message': 'Item added to order'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove_order_item(self, request, pk):
        """Delete request for a user to remove an item from an order"""

        orderitem_id = request.data.get("order_item")
        if not orderitem_id:
            return Response({"error": "Order item ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order_item = OrderItem.objects.get(pk=orderitem_id, order__pk=pk)
            order_item.delete()
            return Response({"message": "Order item removed"}, status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response({"error": "Order item not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderItemSerializer(serializers.ModelSerializer):
    """JSON serializer for order items"""

    price = serializers.ReadOnlyField(source='item.price')
    name = serializers.ReadOnlyField(source='item.name')
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'item', 'quantity')
        depth = 1

class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for orders"""
    items = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id', 'user', 'name', 'open', 'phone', 'email', 'type', 'items')
        depth = 1

    # Serializes order items
    def get_items(self, order):
        """method for getting all items"""
        items_data = [
            {'id': order_item.item.id,
              'name': order_item.item.name,
              'price': order_item.item.price,
              'quantity': order_item.quantity,
              'order_item_id': order_item.id} 
            for order_item in order.items.all()]
        return items_data

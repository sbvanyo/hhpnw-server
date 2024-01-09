"""View module for handling requests about revenue"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hhpnwapi.models import Revenue


class RevenueView(ViewSet):
    """hhpnw revenue view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single revenue.
        Returns: Response -- JSON serialized revenue"""
        
        revenue = Revenue.objects.get(pk=pk)
        serializer = RevenueSerializer(revenue)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all revenue nodes.
        Returns: Response -- JSON serialized list of revenue nodes"""
        revenues = Revenue.objects.all()
        serializer = RevenueSerializer(revenues, many=True)
        return Response(serializer.data)




class RevenueSerializer(serializers.ModelSerializer):
    """JSON serializer for revenue nodes"""
    class Meta:
        model = Revenue
        fields = ('id', 'order', 'date', 'payment', 'subtotal', 'tip', 'total')
        depth = 1

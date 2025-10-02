from django.shortcuts import render
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


# I prefer the Django-Filters package for view filtering, but this'll do

class OrderListBetweenDatesView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        start_date = request.query_params.get("start_date")
        embargo_date = request.query_params.get("embargo_date")
        orders = self.queryset.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status=200)

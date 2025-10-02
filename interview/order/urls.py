from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrderListBetweenDatesView


urlpatterns = [
    path("tags/", OrderTagListCreateView.as_view(), name="order-detail"),
    path("between-dates/", OrderListBetweenDatesView.as_view(), name="order-list-between-dates"),
    path("", OrderListCreateView.as_view(), name="order-list"),
]

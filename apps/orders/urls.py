from django.urls import path
from .views import CheckoutView, MyOrdersView, AdminOrdersView, AdminOrderStatusView

urlpatterns = [
    path('orders/checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/mine/', MyOrdersView.as_view(), name='my_orders'),
    path('admin/orders/', AdminOrdersView.as_view(), name='admin_orders'),
    path('admin/orders/<int:order_id>/status/', AdminOrderStatusView.as_view(), name='admin_order_status'),
]

from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='cart_add'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='cart_remove'),
]

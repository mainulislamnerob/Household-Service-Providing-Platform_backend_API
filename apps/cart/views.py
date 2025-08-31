from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer, RemoveFromCartSerializer

User = get_user_model()

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)

class AddToCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = AddToCartSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        service = ser.validated_data["service"]
        quantity = ser.validated_data["quantity"]
        cart = get_or_create_cart(request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart, service=service,
            defaults={"quantity": quantity, "unit_price": service.base_price}
        )
        if not created:
            item.quantity += quantity
            item.save()

        return Response({"detail":"Added to cart"}, status=status.HTTP_201_CREATED)

class RemoveFromCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = RemoveFromCartSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        cart = get_or_create_cart(request.user)
        item = cart.items.filter(id=ser.validated_data["item_id"]).first()
        if not item:
            return Response({"detail":"Item not found in cart"}, status=404)
        item.delete()
        return Response({"detail":"Removed from cart"})

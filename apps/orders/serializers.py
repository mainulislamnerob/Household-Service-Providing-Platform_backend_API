from rest_framework import serializers
from .models import Order, OrderItem
from apps.cart.models import Cart, CartItem
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)
    class Meta:
        model = OrderItem
        fields = ("id","service","service_name","quantity","unit_price")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id","status","payment_status","payment_ref","total_amount","created_at","items")

class CheckoutSerializer(serializers.Serializer):
    # future: address fields, preferred time, notes, etc.
    note = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        user = self.context["request"].user
        from apps.cart.views import get_or_create_cart
        cart = get_or_create_cart(user)
        if cart.items.count() == 0:
            raise serializers.ValidationError("Cart is empty")

        order = Order.objects.create(user=user, status="PENDING", payment_status="UNPAID")
        total = Decimal("0.00")
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order, service=item.service,
                quantity=item.quantity, unit_price=item.unit_price
            )
            total += item.line_total()
        order.total_amount = total
        order.save()
        cart.items.all().delete()
        return order

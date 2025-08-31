from rest_framework import serializers
from .models import Cart, CartItem
from apps.services.models import Service

class CartItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)
    service_slug = serializers.CharField(source="service.slug", read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id","service","service_name","service_slug","quantity","unit_price","line_total")
        read_only_fields = ("id","service_name","service_slug","line_total")

    def get_line_total(self, obj):
        return str(obj.line_total())

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id","items","total")

    def get_total(self, obj):
        total = sum([i.line_total() for i in obj.items.all()])
        return str(total)

class AddToCartSerializer(serializers.Serializer):
    service_slug = serializers.SlugField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, data):
        from apps.services.models import Service
        service = Service.objects.filter(slug=data["service_slug"], is_active=True).first()
        if not service:
            raise serializers.ValidationError("Service not found")
        data["service"] = service
        return data

class RemoveFromCartSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()

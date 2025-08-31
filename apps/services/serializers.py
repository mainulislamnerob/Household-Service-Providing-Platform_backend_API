from rest_framework import serializers
from django.db.models import Avg
from .models import Service
from apps.reviews.models import Review

class ServiceSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ("id","name","slug","description","base_price","is_active","avg_rating")

    def get_avg_rating(self, obj):
        val = Review.objects.filter(service=obj).aggregate(avg=Avg("rating"))["avg"]
        return round(val, 2) if val else None

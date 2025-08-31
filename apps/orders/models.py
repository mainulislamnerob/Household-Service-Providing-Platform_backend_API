from django.db import models
from django.contrib.auth import get_user_model
from apps.services.models import Service

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING","PENDING"),
        ("CONFIRMED","CONFIRMED"),
        ("FULFILLED","FULFILLED"),
        ("CANCELLED","CANCELLED"),
    )
    PAYMENT_STATUS = (
        ("UNPAID","UNPAID"),
        ("PAID","PAID"),
        ("REFUNDED","REFUNDED"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="UNPAID")
    payment_ref = models.CharField(max_length=64, blank=True)  # placeholder for gateway ref
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order#{self.id} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.quantity * self.unit_price

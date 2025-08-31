from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id","name","base_price","is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

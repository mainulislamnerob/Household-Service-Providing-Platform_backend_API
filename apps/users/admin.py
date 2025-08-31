from django.contrib import admin
from .models import User, Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","email","role","is_staff","is_active")
    search_fields = ("email",)
    list_filter = ("role","is_staff","is_active")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id","user","avatar_url")
    search_fields = ("user__email",)

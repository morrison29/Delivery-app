from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Adds the delivery-agent checkbox and phone number to the user edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Delivery', {'fields': ('is_delivery_agent', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Delivery', {'fields': ('is_delivery_agent', 'phone_number')}),
    )
    list_display = ('username', 'is_delivery_agent', 'phone_number', 'is_staff')
    list_filter = UserAdmin.list_filter + ('is_delivery_agent',)
from django.contrib import admin
from .models import ResaleListing, ResaleTransaction, TicketVerification

# Try registering a simple test model first
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'resale_marketplace'

@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    ordering = ['-created_at']

# Gradually re-enable models to test
@admin.register(ResaleListing)
class ResaleListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'verification_status', 'listed_at']
    list_filter = ['status', 'verification_status']
    search_fields = []  # Remove relationship-based search
    ordering = ['-listed_at']

# @admin.register(ResaleTransaction)
# class ResaleTransactionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'buyer', 'seller', 'amount', 'status', 'created_at']
#     list_filter = ['status']
#     search_fields = ['buyer__username', 'seller__username']
#     ordering = ['-created_at']

# @admin.register(TicketVerification)
# class TicketVerificationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'verification_code', 'status', 'verified_at']
#     list_filter = ['status']
#     search_fields = ['verification_code']
#     ordering = ['-verified_at']

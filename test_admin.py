from django.contrib import admin
from django.db import models

# Create a simple test model to isolate the issue
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

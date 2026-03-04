from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class MerchandiseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Merchandise Categories"

class MerchandiseItem(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('out_of_stock', 'Out of Stock'),
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchandise')
    category = models.ForeignKey(MerchandiseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    
    # Images
    image = models.ImageField(upload_to='merchandise_images/', blank=True, null=True)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchandise:detail', kwargs={'pk': self.pk})
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    @property
    def is_available(self):
        return self.status == 'active' and self.is_in_stock

class MerchandiseVariant(models.Model):
    item = models.ForeignKey(MerchandiseItem, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)  # e.g., "Small", "Medium", "Large" or "Red", "Blue"
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.item.name} - {self.name}"
    
    @property
    def final_price(self):
        return self.item.price + self.price_adjustment
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

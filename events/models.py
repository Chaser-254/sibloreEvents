from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Event(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    
    # Event details
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Regular ticket price")
    vip_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="VIP ticket price (optional)")
    early_bird_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Early bird price (optional)")
    early_bird_deadline = models.DateTimeField(null=True, blank=True, help_text="Early bird deadline")
    
    # Capacity
    max_attendees = models.PositiveIntegerField(help_text="Maximum total attendees")
    max_vip_attendees = models.PositiveIntegerField(default=0, help_text="Maximum VIP attendees (0 for unlimited)")
    current_attendees = models.PositiveIntegerField(default=0)
    current_vip_attendees = models.PositiveIntegerField(default=0)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})
    
    @property
    def is_sold_out(self):
        return (self.current_attendees >= self.max_attendees and 
                (self.max_vip_attendees == 0 or self.current_vip_attendees >= self.max_vip_attendees))
    
    @property
    def available_tickets(self):
        return self.max_attendees - self.current_attendees
    
    @property
    def available_vip_tickets(self):
        if self.max_vip_attendees == 0:
            return "Unlimited"
        return self.max_vip_attendees - self.current_vip_attendees
    
    @property
    def is_vip_sold_out(self):
        return self.max_vip_attendees > 0 and self.current_vip_attendees >= self.max_vip_attendees
    
    @property
    def current_price(self):
        if self.early_bird_price and self.early_bird_deadline:
            from django.utils import timezone
            if timezone.now() <= self.early_bird_deadline:
                return self.early_bird_price
        return self.price
    
    @property
    def current_vip_price(self):
        if self.early_bird_price and self.early_bird_deadline and self.vip_price:
            from django.utils import timezone
            if timezone.now() <= self.early_bird_deadline:
                # Apply early bird discount to VIP tickets as well
                discount_percentage = (self.price - self.early_bird_price) / self.price
                early_bird_vip_price = self.vip_price * (1 - discount_percentage)
                return round(early_bird_vip_price, 2)
        return self.vip_price

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from tickets.models import Ticket
from events.models import Event


class ResaleListing(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    )
    
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )
    
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='resale_listing')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resale_listings')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchased_resale_tickets')
    
    original_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Original ticket price")
    resale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Resale price")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    
    description = models.TextField(blank=True, help_text="Additional information about the ticket")
    contact_preference = models.CharField(
        max_length=20,
        choices=[
            ('platform', 'Platform Transfer'),
            ('in_person', 'In Person'),
            ('both', 'Both'),
        ],
        default='platform',
        help_text="How you prefer to transfer the ticket"
    )
    
    listed_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        help_text="Listing expires 7 days after listing unless sold"
    )
    sold_at = models.DateTimeField(null=True, blank=True)
    
    verification_notes = models.TextField(blank=True, help_text="Admin notes about verification")
    
    class Meta:
        ordering = ['-listed_at']
    
    def __str__(self):
        return f"ResaleListing #{self.id}"
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        
        # Validate price limits (max 20% above original price)
        if self.original_price and self.resale_price:
            max_allowed = self.original_price * Decimal('1.20')  # 20% maximum
            if self.resale_price > max_allowed:
                self.resale_price = max_allowed
        
        super().save(*args, **kwargs)
    
    def get_price_percentage(self):
        if self.original_price:
            return (self.resale_price / self.original_price) * 100
        return 0
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def can_be_purchased(self, user):
        return (
            self.status == 'active' and 
            self.verification_status == 'verified' and 
            not self.is_expired() and 
            user != self.seller
        )
    
    def mark_as_sold(self, buyer):
        self.buyer = buyer
        self.status = 'sold'
        self.sold_at = timezone.now()
        self.ticket.buyer = buyer
        self.ticket.save()
        self.save()


class ResaleTransaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    )
    
    listing = models.OneToOneField(ResaleListing, on_delete=models.CASCADE, related_name='transaction')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resale_purchases')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resale_sales')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True, help_text="Transaction notes and communication")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"ResaleTransaction #{self.id}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            import uuid
            self.transaction_id = f"RS-{uuid.uuid4().hex[:12].upper()}"
        
        # Calculate platform fee (5% of resale price)
        if not self.platform_fee and self.amount:
            self.platform_fee = self.amount * Decimal('0.05')
            self.net_amount = self.amount - self.platform_fee
        
        super().save(*args, **kwargs)
    
    def mark_as_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class TicketVerification(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('invalid', 'Invalid'),
        ('used', 'Already Used'),
    )
    
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='verification')
    verification_code = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_tickets'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    qr_code = models.ImageField(upload_to='resale_qr_codes/', blank=True, null=True)
    
    notes = models.TextField(blank=True, help_text="Verification notes")
    
    class Meta:
        ordering = ['-verified_at']
    
    def __str__(self):
        return f"Verification: {self.ticket} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.verification_code:
            import uuid
            self.verification_code = uuid.uuid4().hex
        
        super().save(*args, **kwargs)
    
    def verify_ticket(self, verified_by):
        self.status = 'verified'
        self.verified_by = verified_by
        self.verified_at = timezone.now()
        self.save()

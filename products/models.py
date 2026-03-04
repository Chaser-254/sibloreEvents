from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Product Categories"

class Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    )
    
    AFFILIATE_COMMISSION_CHOICES = (
        ('5', '5%'),
        ('10', '10%'),
        ('15', '15%'),
        ('20', '20%'),
        ('25', '25%'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, help_text="Brief description for listings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Product details
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    brand = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    dimensions = models.CharField(max_length=100, blank=True, help_text="L x W x H in cm")
    
    # Pricing
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Your cost (not shown to customers)")
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5, help_text="Alert when stock reaches this level")
    track_inventory = models.BooleanField(default=True)
    
    # Affiliate settings
    enable_affiliate = models.BooleanField(default=True, help_text="Enable affiliate marketing for this product")
    affiliate_commission = models.CharField(max_length=2, choices=AFFILIATE_COMMISSION_CHOICES, default='10')
    
    # Shipping
    free_shipping = models.BooleanField(default=False)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Media
    featured_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False, help_text="Digital product (no shipping)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})
    
    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.regular_price
    
    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price < self.regular_price
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.min_stock_level
    
    @property
    def discount_percentage(self):
        if self.is_on_sale:
            return round(((self.regular_price - self.sale_price) / self.regular_price) * 100, 0)
        return 0
    
    @property
    def affiliate_commission_amount(self):
        commission_rate = int(self.affiliate_commission) / 100
        return round(self.current_price * commission_rate, 2)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.title} - Image {self.order}"

class AffiliateLink(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='affiliate_links')
    affiliate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='affiliate_links')
    unique_code = models.CharField(max_length=50, unique=True)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'affiliate']
    
    def __str__(self):
        return f"{self.affiliate.username} - {self.product.title}"
    
    def save(self, *args, **kwargs):
        if not self.unique_code:
            import uuid
            self.unique_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    
    @property
    def affiliate_url(self):
        return f"{self.product.get_absolute_url()}?ref={self.unique_code}"
    
    @property
    def conversion_rate(self):
        if self.clicks > 0:
            return round((self.conversions / self.clicks) * 100, 2)
        return 0

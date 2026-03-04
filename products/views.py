from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .models import Product, ProductCategory, AffiliateLink

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(status='published')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(brand__icontains=search_query)
            )
        
        # Category filter
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(current_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(current_price__lte=max_price)
        
        # Sort options
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['price_low', 'price_high', 'name', '-created_at']:
            if sort_by == 'price_low':
                queryset = queryset.order_by('current_price')
            elif sort_by == 'price_high':
                queryset = queryset.order_by('-current_price')
            elif sort_by == 'name':
                queryset = queryset.order_by('title')
            else:
                queryset = queryset.order_by(sort_by)
        
        return queryset.select_related('seller', 'category').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
        
        # Handle affiliate tracking
        ref_code = self.request.GET.get('ref')
        if ref_code:
            try:
                affiliate_link = AffiliateLink.objects.get(unique_code=ref_code)
                affiliate_link.clicks += 1
                affiliate_link.save()
                context['affiliate_code'] = ref_code
                context['affiliate_info'] = affiliate_link
            except AffiliateLink.DoesNotExist:
                pass
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(status='published').select_related('seller', 'category').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Handle affiliate tracking
        ref_code = self.request.GET.get('ref')
        if ref_code:
            try:
                affiliate_link = AffiliateLink.objects.get(unique_code=ref_code, product=product)
                context['affiliate_code'] = ref_code
                context['affiliate_info'] = affiliate_link
                
                # If user is logged in and is the affiliate, show their stats
                if self.request.user.is_authenticated and self.request.user == affiliate_link.affiliate:
                    context['is_my_affiliate_link'] = True
            except AffiliateLink.DoesNotExist:
                pass
        
        # Get related products
        context['related_products'] = Product.objects.filter(
            category=product.category,
            status='published'
        ).exclude(pk=product.pk)[:4]
        
        # Check if user can become affiliate
        if self.request.user.is_authenticated and self.request.user != product.seller:
            context['can_become_affiliate'] = True
            
        return context

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['title', 'short_description', 'description', 'category', 'sku', 'brand', 
              'weight', 'dimensions', 'regular_price', 'sale_price', 'cost_price',
              'stock_quantity', 'min_stock_level', 'track_inventory', 'enable_affiliate',
              'affiliate_commission', 'free_shipping', 'shipping_cost', 'featured_image',
              'meta_title', 'meta_description', 'is_digital']
    success_url = reverse_lazy('products:list')
    
    def test_func(self):
        return self.request.user.is_product_seller
    
    def handle_no_permission(self):
        messages.error(self.request, 'You need a product seller account to create products.')
        return super().handle_no_permission()
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        form.instance.status = 'published'  # Auto-publish new products
        messages.success(self.request, 'Product created successfully!')
        return super().form_valid(form)

class MyProductsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'products/my_products.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def test_func(self):
        return self.request.user.is_product_seller
    
    def handle_no_permission(self):
        messages.error(self.request, 'You need a product seller account to view your products.')
        return super().handle_no_permission()
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).select_related('category').order_by('-created_at')

class AffiliateDashboardView(LoginRequiredMixin, ListView):
    model = AffiliateLink
    template_name = 'products/affiliate_dashboard.html'
    context_object_name = 'affiliate_links'
    paginate_by = 20
    
    def get_queryset(self):
        return AffiliateLink.objects.filter(affiliate=self.request.user).select_related('product').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        affiliate_links = self.get_queryset()
        
        # Calculate totals
        total_clicks = sum(link.clicks for link in affiliate_links)
        total_conversions = sum(link.conversions for link in affiliate_links)
        total_commission = sum(link.commission_earned for link in affiliate_links)
        
        context['total_clicks'] = total_clicks
        context['total_conversions'] = total_conversions
        context['total_commission'] = total_commission
        context['total_products'] = affiliate_links.count()
        
        # Available products to promote
        context['available_products'] = Product.objects.filter(
            status='published',
            enable_affiliate=True
        ).exclude(
            affiliate_links__affiliate=self.request.user
        ).select_related('seller', 'category')[:10]
        
        return context

@method_decorator(require_POST, name='dispatch')
class CreateAffiliateLinkView(LoginRequiredMixin, CreateView):
    model = AffiliateLink
    fields = []  # No fields needed, created automatically
    
    def form_valid(self, form):
        product_id = self.request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id, status='published', enable_affiliate=True)
        
        # Check if affiliate link already exists
        existing_link = AffiliateLink.objects.filter(product=product, affiliate=self.request.user).first()
        if existing_link:
            return JsonResponse({'success': False, 'message': 'You already have an affiliate link for this product'})
        
        # Create new affiliate link
        affiliate_link = AffiliateLink.objects.create(
            product=product,
            affiliate=self.request.user
        )
        
        return JsonResponse({
            'success': True, 
            'affiliate_url': affiliate_link.affiliate_url,
            'unique_code': affiliate_link.unique_code
        })

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from .forms import CustomUserCreationForm, UserProfileForm
from .models import User

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.is_product_seller:
            return reverse_lazy('accounts:product_seller_dashboard')
        elif user.is_seller:
            return reverse_lazy('accounts:seller_dashboard')
        return reverse_lazy('accounts:buyer_dashboard')

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logged out successfully.')
        return super().dispatch(request, *args, **kwargs)
    
    def get_next_page(self):
        return reverse_lazy('home')

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created! Please log in.')
        return response

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated!')
        return super().form_valid(form)

@login_required
def buyer_dashboard(request):
    return render(request, 'accounts/buyer_dashboard.html')

@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('home')
    
    from events.models import Event
    from merchandise.models import MerchandiseItem
    from tickets.models import Ticket, MerchandiseOrder
    
    # Get seller's statistics
    total_events = Event.objects.filter(organizer=request.user).count()
    total_merchandise = MerchandiseItem.objects.filter(seller=request.user).count()
    
    # Get recent tickets for seller's events
    recent_tickets = Ticket.objects.filter(
        event__organizer=request.user,
        payment_status='paid'
    ).order_by('-created_at')[:5]
    
    # Calculate total revenue
    ticket_revenue = Ticket.objects.filter(
        event__organizer=request.user,
        payment_status='paid'
    ).aggregate(
        total=models.Sum('total_amount')
    )['total'] or 0
    
    context = {
        'total_events': total_events,
        'total_merchandise': total_merchandise,
        'recent_tickets': recent_tickets,
        'ticket_revenue': ticket_revenue,
    }
    
    return render(request, 'accounts/seller_dashboard.html', context)

@login_required
def product_seller_dashboard(request):
    if not request.user.is_product_seller:
        messages.error(request, 'Access denied. Product seller account required.')
        return redirect('home')
    
    from products.models import Product, AffiliateLink
    
    # Get product seller's statistics
    total_products = Product.objects.filter(seller=request.user).count()
    
    # Get affiliate statistics
    affiliate_links = AffiliateLink.objects.filter(affiliate=request.user)
    total_affiliate_links = affiliate_links.count()
    total_clicks = sum(link.clicks for link in affiliate_links)
    total_commission = sum(link.commission_earned for link in affiliate_links)
    
    # Get recent products
    recent_products = Product.objects.filter(
        seller=request.user
    ).order_by('-created_at')[:5]
    
    # Get top performing products
    top_products = Product.objects.filter(
        seller=request.user
    ).annotate(
        total_clicks=models.Sum('affiliate_links__clicks'),
        total_conversions=models.Sum('affiliate_links__conversions'),
        total_commission=models.Sum('affiliate_links__commission_earned')
    ).order_by('-total_commission')[:5]
    
    context = {
        'total_products': total_products,
        'total_affiliate_links': total_affiliate_links,
        'total_clicks': total_clicks,
        'total_commission': total_commission,
        'recent_products': recent_products,
        'top_products': top_products,
    }
    
    return render(request, 'accounts/product_seller_dashboard.html', context)

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Logout the user first
        from django.contrib.auth import logout
        logout(request)
        
        # Delete the user account
        user.delete()
        
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('home')
    
    return render(request, 'accounts/delete_profile_confirm.html')

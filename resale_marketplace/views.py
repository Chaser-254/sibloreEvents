from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal
from .models import ResaleListing, ResaleTransaction, TicketVerification
from tickets.models import Ticket


def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


class VerificationQueueView(LoginRequiredMixin, ListView):
    model = TicketVerification
    template_name = 'resale_marketplace/verification_queue.html'
    context_object_name = 'verifications'
    paginate_by = 20
    
    @user_passes_test(is_admin_or_staff)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return TicketVerification.objects.filter(
            status='pending'
        ).select_related('ticket__event', 'ticket__resale_listing', 'verified_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = self.get_queryset().count()
        return context


@login_required
@user_passes_test(is_admin_or_staff)
def verify_ticket(request, pk):
    verification = get_object_or_404(TicketVerification, pk=pk)
    
    if request.method == 'POST':
        verification.status = 'verified'
        verification.verified_by = request.user
        verification.verified_at = timezone.now()
        verification.save()
        
        # Update listing status
        if verification.ticket.resale_listing:
            verification.ticket.resale_listing.verification_status = 'verified'
            verification.ticket.resale_listing.save()
        
        messages.success(request, f'Ticket verification for {verification.ticket.event.name} completed.')
        return redirect('resale_marketplace:verification_queue')
    
    return render(request, 'resale_marketplace/verify_ticket.html', {'verification': verification})


@login_required
@user_passes_test(is_admin_or_staff)
def reject_ticket(request, pk):
    verification = get_object_or_404(TicketVerification, pk=pk)
    
    if request.method == 'POST':
        verification.status = 'invalid'
        verification.verified_by = request.user
        verification.verified_at = timezone.now()
        verification.save()
        
        # Update listing status
        if verification.ticket.resale_listing:
            verification.ticket.resale_listing.verification_status = 'rejected'
            verification.ticket.resale_listing.save()
        
        messages.warning(request, f'Ticket verification for {verification.ticket.event.name} rejected.')
        return redirect('resale_marketplace:verification_queue')
    
    return render(request, 'resale_marketplace/reject_ticket.html', {'verification': verification})


class ResaleMarketplaceView(ListView):
    model = ResaleListing
    template_name = 'resale_marketplace/marketplace.html'
    context_object_name = 'listings'
    paginate_by = 12
    
    def get_queryset(self):
        return ResaleListing.objects.filter(
            status='active',
            verification_status='verified'
        ).select_related('ticket__event', 'seller')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_listings'] = self.get_queryset().count()
        return context


class MyResaleListingsView(LoginRequiredMixin, ListView):
    model = ResaleListing
    template_name = 'resale_marketplace/my_listings.html'
    context_object_name = 'listings'
    paginate_by = 10
    
    def get_queryset(self):
        return ResaleListing.objects.filter(
            seller=self.request.user
        ).select_related('ticket__event', 'seller')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_listings'] = self.get_queryset().filter(status='active').count()
        context['sold_listings'] = self.get_queryset().filter(status='sold').count()
        return context


class CreateResaleListingView(LoginRequiredMixin, CreateView):
    model = ResaleListing
    template_name = 'resale_marketplace/create_listing.html'
    fields = ['ticket', 'resale_price', 'description', 'contact_preference']
    success_url = reverse_lazy('resale_marketplace:my_listings')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show tickets owned by user that aren't already listed
        tickets = Ticket.objects.filter(
            buyer=self.request.user,
            resale_listing__isnull=True
        ).select_related('event')
        form.fields['ticket'].queryset = tickets
        
        # Add data attributes to options for JavaScript
        form.fields['ticket'].widget.attrs.update({'onchange': 'updatePriceInfo()'})
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add tickets with price info for JavaScript
        tickets = Ticket.objects.filter(
            buyer=self.request.user,
            resale_listing__isnull=True
        ).select_related('event')
        context['available_tickets'] = tickets
        return context
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        form.instance.original_price = form.instance.ticket.price_per_ticket
        
        # Validate price limits
        max_allowed = form.instance.original_price * Decimal('1.20')  # 20% maximum
        if form.instance.resale_price > max_allowed:
            form.instance.resale_price = max_allowed
            messages.warning(
                self.request, 
                f'Price adjusted to maximum allowed ({max_allowed:.2f} - 20% above original price)'
            )
        
        messages.success(self.request, 'Your ticket has been listed for resale and is pending verification.')
        return super().form_valid(form)


class ResaleListingDetailView(DetailView):
    model = ResaleListing
    template_name = 'resale_marketplace/listing_detail.html'
    context_object_name = 'listing'
    
    def get_queryset(self):
        return ResaleListing.objects.filter(
            status='active',
            verification_status='verified'
        ).select_related('ticket__event', 'seller')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_purchase'] = self.object.can_be_purchased(self.request.user)
        context['price_percentage'] = self.object.get_price_percentage()
        return context


@login_required
def purchase_ticket(request, pk):
    listing = get_object_or_404(ResaleListing, pk=pk)
    
    if not listing.can_be_purchased(request.user):
        messages.error(request, 'This ticket cannot be purchased.')
        return redirect('resale_marketplace:listing_detail', pk=pk)
    
    if request.method == 'POST':
        # Create transaction
        transaction = ResaleTransaction.objects.create(
            listing=listing,
            buyer=request.user,
            seller=listing.seller,
            amount=listing.resale_price
        )
        
        messages.success(
            request, 
            f'Purchase initiated! Transaction ID: {transaction.transaction_id}. '
            'Please complete payment to finalize the purchase.'
        )
        return redirect('resale_marketplace:transaction_detail', transaction_id=transaction.transaction_id)
    
    return render(request, 'resale_marketplace/purchase_confirm.html', {
        'listing': listing,
        'transaction': ResaleTransaction(
            listing=listing,
            buyer=request.user,
            seller=listing.seller,
            amount=listing.resale_price
        )
    })


@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(
        ResaleTransaction, 
        transaction_id=transaction_id,
        buyer=request.user
    )
    
    return render(request, 'resale_marketplace/transaction_detail.html', {
        'transaction': transaction
    })


@login_required
def complete_purchase(request, transaction_id):
    transaction = get_object_or_404(
        ResaleTransaction, 
        transaction_id=transaction_id,
        buyer=request.user,
        status='pending'
    )
    
    # In a real implementation, this would integrate with a payment gateway
    # For now, we'll simulate successful payment
    transaction.mark_as_completed()
    transaction.listing.mark_as_sold(request.user)
    
    # Create ticket verification
    TicketVerification.objects.create(
        ticket=transaction.listing.ticket
    )
    
    messages.success(
        request, 
        'Purchase completed successfully! Your ticket has been transferred to your account.'
    )
    return redirect('resale_marketplace:my_purchases')


class MyPurchasesView(LoginRequiredMixin, ListView):
    model = ResaleTransaction
    template_name = 'resale_marketplace/my_purchases.html'
    context_object_name = 'transactions'
    paginate_by = 10
    
    def get_queryset(self):
        return ResaleTransaction.objects.filter(
            buyer=self.request.user
        ).select_related('listing__ticket__event', 'seller')


class CancelListingView(LoginRequiredMixin, UpdateView):
    model = ResaleListing
    template_name = 'resale_marketplace/cancel_listing.html'
    fields = []
    success_url = reverse_lazy('resale_marketplace:my_listings')
    
    def get_queryset(self):
        return ResaleListing.objects.filter(
            seller=self.request.user,
            status='active'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the listing object to context for template access
        context['listing'] = self.object
        return context
    
    def form_valid(self, form):
        form.instance.status = 'cancelled'
        messages.success(self.request, 'Your listing has been cancelled.')
        return super().form_valid(form)


def search_listings(request):
    query = request.GET.get('q', '')
    event_filter = request.GET.get('event', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    
    listings = ResaleListing.objects.filter(
        status='active',
        verification_status='verified'
    ).select_related('ticket__event', 'seller')
    
    if query:
        listings = listings.filter(
            Q(ticket__event__name__icontains=query) |
            Q(ticket__event__description__icontains=query) |
            Q(description__icontains=query)
        )
    
    if event_filter:
        listings = listings.filter(ticket__event__name__icontains=event_filter)
    
    if price_min:
        try:
            listings = listings.filter(resale_price__gte=float(price_min))
        except ValueError:
            pass
    
    if price_max:
        try:
            listings = listings.filter(resale_price__lte=float(price_max))
        except ValueError:
            pass
    
    return render(request, 'resale_marketplace/search_results.html', {
        'listings': listings,
        'query': query,
        'event_filter': event_filter,
        'price_min': price_min,
        'price_max': price_max,
        'total_count': listings.count()
    })

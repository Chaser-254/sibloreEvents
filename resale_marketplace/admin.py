from django.contrib import admin
from .models import ResaleListing, ResaleTransaction, TicketVerification


@admin.register(ResaleListing)
class ResaleListingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'seller', 'original_price', 'resale_price', 
                   'status', 'verification_status', 'listed_at', 'expires_at']
    list_filter = [
        'status', 'verification_status', 'contact_preference', 
        'listed_at', 'expires_at'
    ]
    search_fields = [
        'ticket__event__name', 'seller__username', 'description'
    ]
    date_hierarchy = 'listed_at'
    ordering = ['-listed_at']
    readonly_fields = [
        'original_price', 'listed_at', 'expires_at', 'sold_at'
    ]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('ticket__event', 'seller')
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj and obj.status in ['sold', 'cancelled']:
            readonly.extend(['ticket', 'resale_price', 'description'])
        return readonly


@admin.register(ResaleTransaction)
class ResaleTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id', 'listing', 'buyer', 'seller', 
        'amount', 'platform_fee', 'status', 'created_at'
    ]
    list_filter = [
        'status', 'created_at', 'payment_method'
    ]
    search_fields = [
        'transaction_id', 'buyer__username', 'seller__username',
        'listing__ticket__event__name'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = [
        'transaction_id', 'listing', 'buyer', 'seller', 'amount',
        'platform_fee', 'net_amount', 'created_at', 'completed_at'
    ]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'listing__ticket__event', 
            'buyer', 'seller'
        )


@admin.register(TicketVerification)
class TicketVerificationAdmin(admin.ModelAdmin):
    list_display = [
        'ticket', 'verification_code', 'status', 
        'verified_by', 'verified_at'
    ]
    list_filter = [
        'status', 'verified_at'
    ]
    search_fields = [
        'verification_code', 'ticket__event__name', 
        'verified_by__username'
    ]
    date_hierarchy = 'verified_at'
    ordering = ['-verified_at']
    readonly_fields = [
        'verification_code', 'ticket', 'verified_at'
    ]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'ticket__event', 'verified_by'
        )
    
    actions = ['verify_tickets', 'reject_tickets']
    
    def verify_tickets(self, request, queryset):
        for verification in queryset.filter(status='pending'):
            verification.status = 'verified'
            verification.verified_by = request.user
            verification.verified_at = timezone.now()
            verification.save()
        self.message_user(
            request, 
            f'{queryset.count()} ticket(s) verified successfully.',
            messages.SUCCESS
        )
    verify_tickets.short_description = 'Verify selected tickets'
    
    def reject_tickets(self, request, queryset):
        for verification in queryset.filter(status='pending'):
            verification.status = 'invalid'
            verification.save()
        self.message_user(
            request, 
            f'{queryset.count()} ticket(s) rejected.',
            messages.WARNING
        )
    reject_tickets.short_description = 'Reject selected tickets'

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from decimal import Decimal
from .models import ResaleListing, ResaleTransaction, TicketVerification
from tickets.models import Ticket
from events.models import Event
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


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
        
        # Save the listing first
        response = super().form_valid(form)
        
        # Create ticket verification for admin review
        TicketVerification.objects.create(
            ticket=form.instance.ticket
        )
        
        messages.success(self.request, 'Your ticket has been listed for resale and is pending verification.')
        return response


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


@login_required
def download_receipt(request, transaction_id):
    """Generate PDF receipt for completed transaction"""
    transaction = get_object_or_404(
        ResaleTransaction, 
        transaction_id=transaction_id,
        buyer=request.user,
        status='completed'
    )
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    normal_style = styles['Normal']
    
    # Add title
    story.append(Paragraph("PAYMENT RECEIPT", title_style))
    story.append(Spacer(1, 12))
    
    # Transaction details table
    data = [
        ['Transaction ID:', transaction.transaction_id],
        ['Date:', transaction.completed_at.strftime('%B %d, %Y at %I:%M %p')],
        ['Status:', 'COMPLETED'],
        ['Payment Method:', 'Platform Transfer'],
        ['', ''],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))
    
    # Event details
    story.append(Paragraph("EVENT DETAILS", heading_style))
    story.append(Spacer(1, 6))
    
    event_data = [
        ['Event:', transaction.listing.ticket.event.name],
        ['Date:', transaction.listing.ticket.event.start_date.strftime('%B %d, %Y at %I:%M %p')],
        ['Venue:', transaction.listing.ticket.event.venue],
        ['Quantity:', f"{transaction.listing.ticket.quantity} ticket(s)"],
        ['', ''],
    ]
    
    event_table = Table(event_data, colWidths=[2*inch, 4*inch])
    event_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(event_table)
    story.append(Spacer(1, 12))
    
    # Price breakdown
    story.append(Paragraph("PRICE BREAKDOWN", heading_style))
    story.append(Spacer(1, 6))
    
    price_data = [
        ['Original Price:', f'KES {transaction.listing.original_price}'],
        ['Resale Price:', f'KES {transaction.listing.resale_price}'],
        ['Platform Fee:', f'KES {transaction.platform_fee}'],
        ['Total Amount:', f'KES {transaction.amount}'],
        ['You Saved:', f'KES {transaction.listing.original_price - transaction.listing.resale_price}'],
    ]
    
    price_table = Table(price_data, colWidths=[2*inch, 4*inch])
    price_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
    ]))
    story.append(price_table)
    story.append(Spacer(1, 20))
    
    # Party information
    story.append(Paragraph("PARTY INFORMATION", heading_style))
    story.append(Spacer(1, 6))
    
    party_data = [
        ['Seller:', transaction.seller.username],
        ['Buyer:', transaction.buyer.username],
        ['Contact:', 'support@sibloreevents.com'],
    ]
    
    party_table = Table(party_data, colWidths=[2*inch, 4*inch])
    party_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(party_table)
    story.append(Spacer(1, 30))
    
    # Footer
    story.append(Paragraph("This is an automatically generated receipt. For any questions, please contact our support team.", normal_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    # Create response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{transaction.transaction_id}.pdf"'
    return response


@login_required
def download_ticket(request, transaction_id):
    """Generate PDF ticket for completed transaction"""
    transaction = get_object_or_404(
        ResaleTransaction, 
        transaction_id=transaction_id,
        buyer=request.user,
        status='completed'
    )
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    normal_style = styles['Normal']
    
    # Add title
    story.append(Paragraph("EVENT TICKET", title_style))
    story.append(Spacer(1, 12))
    
    # Event details
    story.append(Paragraph("EVENT INFORMATION", heading_style))
    story.append(Spacer(1, 6))
    
    event_data = [
        ['Event Name:', transaction.listing.ticket.event.name],
        ['Date:', transaction.listing.ticket.event.start_date.strftime('%B %d, %Y')],
        ['Time:', transaction.listing.ticket.event.start_date.strftime('%I:%M %p')],
        ['Venue:', transaction.listing.ticket.event.venue],
        ['Address:', transaction.listing.ticket.event.address],
        ['City:', transaction.listing.ticket.event.city],
        ['Quantity:', f"{transaction.listing.ticket.quantity} ticket(s)"],
        ['Ticket Type:', 'RESALE TICKET'],
        ['Ticket ID:', transaction.transaction_id],
        ['', ''],
    ]
    
    event_table = Table(event_data, colWidths=[2*inch, 4*inch])
    event_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, -2), (-1, -2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -2), (-1, -2), 12),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
    ]))
    story.append(event_table)
    story.append(Spacer(1, 12))
    
    # Attendee information
    story.append(Paragraph("ATTENDEE INFORMATION", heading_style))
    story.append(Spacer(1, 6))
    
    attendee_data = [
        ['Name:', transaction.buyer.username],
        ['Email:', transaction.buyer.email],
        ['Purchase Date:', transaction.completed_at.strftime('%B %d, %Y')],
        ['Purchase ID:', transaction.transaction_id],
        ['', ''],
    ]
    
    attendee_table = Table(attendee_data, colWidths=[2*inch, 4*inch])
    attendee_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(attendee_table)
    story.append(Spacer(1, 20))
    
    # QR Code placeholder (in real implementation, generate actual QR code)
    story.append(Paragraph("SCAN FOR ENTRY", heading_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("QR Code would be generated here with ticket verification details", normal_style))
    story.append(Spacer(1, 12))
    
    # Important information
    story.append(Paragraph("IMPORTANT INFORMATION", heading_style))
    story.append(Spacer(1, 6))
    
    info_text = """
    • Please arrive 30 minutes before the event start time
    • Bring a valid ID along with this ticket
    • This ticket is non-transferable and non-refundable
    • For any issues, contact support@sibloreevents.com
    • Keep this ticket safe - replacement may incur fees
    """
    
    story.append(Paragraph(info_text, normal_style))
    story.append(Spacer(1, 30))
    
    # Footer
    story.append(Paragraph("Generated by SibloreEvents Platform", normal_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    # Create response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{transaction.transaction_id}.pdf"'
    return response

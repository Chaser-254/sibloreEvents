from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.decorators.http import require_POST
from django.db import transaction
from events.models import Event
from .models import Ticket
from .forms import TicketPurchaseForm

class MyTicketsView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/my_tickets.html'
    context_object_name = 'tickets'
    paginate_by = 10
    
    def get_queryset(self):
        return Ticket.objects.filter(
            buyer=self.request.user
        ).select_related('event', 'event__organizer').order_by('-created_at')

class TicketPrintView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_print.html'
    context_object_name = 'ticket'
    pk_url_kwarg = 'ticket_id'
    
    def get_queryset(self):
        return Ticket.objects.filter(
            buyer=self.request.user
        ).select_related('event', 'event__organizer')
    
    def dispatch(self, request, *args, **kwargs):
        # Return the template directly for printing/downloading
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'
    pk_url_kwarg = 'ticket_id'
    
    def get_queryset(self):
        return Ticket.objects.filter(
            buyer=self.request.user
        ).select_related('event', 'event__organizer')

class TicketPurchaseView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'tickets/ticket_purchase.html'
    form_class = TicketPurchaseForm
    success_url = reverse_lazy('tickets:my_tickets')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, id=event_id, status='published')
        context['event'] = event
        return context
    
    def form_valid(self, form):
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, id=event_id, status='published')
        
        # Check if event is sold out
        if event.is_sold_out:
            messages.error(self.request, 'This event is sold out!')
            return redirect('events:detail', pk=event.pk)
        
        quantity = form.cleaned_data['quantity']
        
        # Check if requested quantity is available
        if quantity > event.available_tickets:
            messages.error(self.request, f'Only {event.available_tickets} tickets available!')
            return self.form_invalid(form)
        
        # Create ticket
        with transaction.atomic():
            ticket = form.save(commit=False)
            ticket.event = event
            ticket.buyer = self.request.user
            ticket.price_per_ticket = event.current_price
            ticket.total_amount = event.current_price * quantity
            ticket.save()
            
            # For now, we'll mark as paid (simulating payment)
            # In production, this would be handled by payment gateway
            ticket.mark_as_paid()
        
        messages.success(self.request, f'Successfully purchased {quantity} ticket(s) for {event.title}!')
        return redirect('tickets:detail', ticket_id=ticket.id)

@require_POST
@login_required
def simulate_payment(request, ticket_id):
    """Simulate payment processing for demo purposes"""
    ticket = get_object_or_404(Ticket, id=ticket_id, buyer=request.user)
    
    if ticket.payment_status == 'paid':
        messages.warning(request, 'This ticket has already been paid for!')
        return redirect('tickets:detail', ticket_id=ticket.id)
    
    # Simulate payment processing
    ticket.mark_as_paid()
    messages.success(request, 'Payment processed successfully!')
    
    return redirect('tickets:detail', ticket_id=ticket.id)

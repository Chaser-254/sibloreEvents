from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Event, Category
from merchandise.models import MerchandiseItem

class MyEventsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'events/my_events.html'
    context_object_name = 'events'
    paginate_by = 12
    
    def test_func(self):
        return self.request.user.is_seller
    
    def handle_no_permission(self):
        messages.error(self.request, 'You need a seller account to view your events.')
        return super().handle_no_permission()
    
    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user).select_related('category').order_by('-created_at')

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Event.objects.filter(status='published')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(venue__icontains=search_query) |
                Q(city__icontains=search_query)
            )
        
        # Category filter
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset.select_related('organizer', 'category').prefetch_related('tickets')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        return Event.objects.filter(status='published').select_related('organizer', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Check if user has already purchased tickets for this event
        if self.request.user.is_authenticated:
            user_tickets = event.tickets.filter(
                buyer=self.request.user,
                payment_status='paid'
            ).first()
            context['user_tickets'] = user_tickets
            context['can_review'] = user_tickets and user_tickets.status == 'confirmed'
        
        # Get related events
        context['related_events'] = Event.objects.filter(
            category=event.category,
            status='published'
        ).exclude(pk=event.pk)[:4]
        
        # Get related merchandise items for this event
        context['event_merchandise'] = MerchandiseItem.objects.filter(
            event=event,
            status='active'
        ).select_related('category')
        
        return context

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'category', 'image', 'start_date', 'end_date', 
              'venue', 'address', 'city', 'country', 'price', 'vip_price', 'early_bird_price', 
              'early_bird_deadline', 'max_attendees', 'max_vip_attendees']
    success_url = reverse_lazy('events:list')
    
    def test_func(self):
        return self.request.user.is_seller
    
    def handle_no_permission(self):
        messages.error(self.request, 'You need a seller account to create events.')
        return super().handle_no_permission()
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        form.instance.status = 'published'  # Auto-publish new events
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'category', 'image', 'start_date', 'end_date', 
              'venue', 'address', 'city', 'country', 'price', 'vip_price', 'early_bird_price', 
              'early_bird_deadline', 'max_attendees', 'max_vip_attendees', 'status']
    
    def test_func(self):
        event = self.get_object()
        return self.request.user.is_seller and event.organizer == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, 'You can only edit your own events.')
        return super().handle_no_permission()
    
    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully!')
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:list')
    
    def test_func(self):
        event = self.get_object()
        return self.request.user.is_seller and event.organizer == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, 'You can only delete your own events.')
        return super().handle_no_permission()
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)

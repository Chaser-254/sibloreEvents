from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import MerchandiseItem, MerchandiseCategory

class MerchandiseListView(ListView):
    model = MerchandiseItem
    template_name = 'merchandise/merchandise_list.html'
    context_object_name = 'merchandise_items'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = MerchandiseItem.objects.filter(status='active')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Category filter
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset.select_related('seller', 'category').prefetch_related('variants')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MerchandiseCategory.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

class MerchandiseDetailView(DetailView):
    model = MerchandiseItem
    template_name = 'merchandise/merchandise_detail.html'
    context_object_name = 'merchandise'
    
    def get_queryset(self):
        return MerchandiseItem.objects.filter(status='active').select_related('seller', 'category').prefetch_related('variants')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        merchandise = self.get_object()
        
        # Get related merchandise
        context['related_items'] = MerchandiseItem.objects.filter(
            category=merchandise.category,
            status='active'
        ).exclude(pk=merchandise.pk)[:4]
        
        return context

class MerchandiseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MerchandiseItem
    template_name = 'merchandise/merchandise_form.html'
    fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'image']
    success_url = reverse_lazy('merchandise:list')
    
    def test_func(self):
        return self.request.user.is_seller
    
    def handle_no_permission(self):
        messages.error(self.request, 'You need a seller account to create merchandise.')
        return super().handle_no_permission()
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, 'Merchandise created successfully!')
        return super().form_valid(form)

class MerchandiseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MerchandiseItem
    template_name = 'merchandise/merchandise_form.html'
    fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'image', 'status']
    
    def test_func(self):
        merchandise = self.get_object()
        return self.request.user.is_seller and merchandise.seller == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, 'You can only edit your own merchandise.')
        return super().handle_no_permission()
    
    def form_valid(self, form):
        messages.success(self.request, 'Merchandise updated successfully!')
        return super().form_valid(form)

class MerchandiseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MerchandiseItem
    template_name = 'merchandise/merchandise_confirm_delete.html'
    success_url = reverse_lazy('merchandise:list')
    
    def test_func(self):
        merchandise = self.get_object()
        return self.request.user.is_seller and merchandise.seller == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, 'You can only delete your own merchandise.')
        return super().handle_no_permission()
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Merchandise deleted successfully!')
        return super().delete(request, *args, **kwargs)

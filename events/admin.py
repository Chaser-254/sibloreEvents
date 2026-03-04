from django.contrib import admin
from .models import Category, Event

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'category', 'start_date', 'venue', 'price', 'vip_price', 'status', 'current_attendees', 'max_attendees', 'current_vip_attendees', 'max_vip_attendees')
    list_filter = ('status', 'category', 'start_date', 'is_featured')
    search_fields = ('title', 'description', 'venue', 'city')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'organizer', 'category', 'image')
        }),
        ('Event Details', {
            'fields': ('start_date', 'end_date', 'venue', 'address', 'city', 'country')
        }),
        ('Pricing', {
            'fields': ('price', 'vip_price', 'early_bird_price', 'early_bird_deadline')
        }),
        ('Capacity', {
            'fields': ('max_attendees', 'max_vip_attendees', 'current_attendees', 'current_vip_attendees')
        }),
        ('Status', {
            'fields': ('status', 'is_featured')
        }),
    )
    
    readonly_fields = ('current_attendees', 'current_vip_attendees')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('organizer', 'category')

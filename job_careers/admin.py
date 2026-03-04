from django.contrib import admin
from .models import JobCategory, JobVacancy, JobApplication


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'job_type', 'experience_level', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'job_type', 'experience_level', 'category', 'is_featured']
    search_fields = ['title', 'description', 'location']
    list_editable = ['status', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'status', 'is_featured')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'responsibilities', 'benefits')
        }),
        ('Location & Type', {
            'fields': ('location', 'job_type', 'experience_level')
        }),
        ('Salary & Deadline', {
            'fields': ('salary_min', 'salary_max', 'application_deadline')
        }),
        ('Meta', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = ['created_at', 'updated_at']
        if not obj:  # creating a new object
            readonly.append('created_by')
        return readonly
    
    def save_model(self, request, obj, form, change):
        if not change:  # creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job', 'email', 'phone', 'status', 'applied_at']
    list_filter = ['status', 'job', 'applied_at']
    search_fields = ['first_name', 'last_name', 'email', 'job__title']
    list_editable = ['status']
    date_hierarchy = 'applied_at'
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Application Details', {
            'fields': ('job', 'cover_letter', 'resume')
        }),
        ('Additional Information', {
            'fields': ('linkedin_profile', 'portfolio')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes', 'applied_at')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['applied_at']
        return []
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'
    
    # Add custom actions
    actions = ['mark_as_reviewed', 'mark_as_shortlisted', 'mark_as_rejected']
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
        self.message_user(request, f'{queryset.count()} applications marked as reviewed.')
    mark_as_reviewed.short_description = 'Mark selected applications as reviewed'
    
    def mark_as_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
        self.message_user(request, f'{queryset.count()} applications marked as shortlisted.')
    mark_as_shortlisted.short_description = 'Mark selected applications as shortlisted'
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} applications marked as rejected.')
    mark_as_rejected.short_description = 'Mark selected applications as rejected'

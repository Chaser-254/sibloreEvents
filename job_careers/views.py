from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from .models import JobVacancy, JobCategory, JobApplication
from .forms import JobApplicationForm


def career_list(request):
    """Display all active job vacancies"""
    featured_jobs = JobVacancy.objects.filter(
        status='active', 
        is_featured=True
    ).exclude(
        Q(application_deadline__lt=timezone.now().date()) | Q(application_deadline__isnull=True)
    )
    
    all_jobs = JobVacancy.objects.filter(
        status='active'
    ).exclude(
        Q(application_deadline__lt=timezone.now().date()) | Q(application_deadline__isnull=True)
    )
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        all_jobs = all_jobs.filter(category__slug=category_slug)
    
    # Filter by job type
    job_type = request.GET.get('type')
    if job_type:
        all_jobs = all_jobs.filter(job_type=job_type)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        all_jobs = all_jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(all_jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = JobCategory.objects.all()
    
    context = {
        'featured_jobs': featured_jobs,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'selected_type': job_type,
        'search_query': search_query,
    }
    return render(request, 'job_careers/career_list.html', context)


def career_detail(request, slug):
    """Display detailed view of a job vacancy"""
    job = get_object_or_404(JobVacancy, slug=slug, status='active')
    
    # Check if job has expired
    if job.is_expired:
        messages.warning(request, "This job vacancy has expired.")
    
    # Get related jobs (same category, excluding current job)
    related_jobs = JobVacancy.objects.filter(
        category=job.category,
        status='active'
    ).exclude(
        id=job.id
    ).exclude(
        Q(application_deadline__lt=timezone.now().date()) | Q(application_deadline__isnull=True)
    )[:4]
    
    # Check if user has already applied
    has_applied = False
    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(
            job=job,
            email=request.user.email
        ).exists()
    
    context = {
        'job': job,
        'related_jobs': related_jobs,
        'has_applied': has_applied,
    }
    return render(request, 'job_careers/career_detail.html', context)


def apply_job(request, slug):
    """Handle job application submission"""
    job = get_object_or_404(JobVacancy, slug=slug, status='active')
    
    if job.is_expired:
        messages.error(request, "This job vacancy has expired and is no longer accepting applications.")
        return redirect('job_careers:detail', slug=slug)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            
            # Check if user has already applied
            existing_application = JobApplication.objects.filter(
                job=job,
                email=application.email
            ).first()
            
            if existing_application:
                messages.warning(request, "You have already applied for this position.")
                return redirect('job_careers:detail', slug=slug)
            
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('job_careers:success')
    else:
        form = JobApplicationForm()
        
        # Pre-fill form if user is logged in
        if request.user.is_authenticated:
            form.fields['first_name'].initial = request.user.first_name
            form.fields['last_name'].initial = request.user.last_name
            form.fields['email'].initial = request.user.email
    
    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'job_careers/apply_job.html', context)


def application_success(request):
    """Display success page after application submission"""
    return render(request, 'job_careers/application_success.html')


@login_required
def manage_applications(request):
    """Allow staff to manage job applications (for admin users)"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    applications = JobApplication.objects.all().order_by('-applied_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Filter by job
    job_filter = request.GET.get('job')
    if job_filter:
        applications = applications.filter(job_id=job_filter)
    
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    jobs = JobVacancy.objects.all()
    
    context = {
        'page_obj': page_obj,
        'jobs': jobs,
        'selected_status': status_filter,
        'selected_job': job_filter,
    }
    return render(request, 'job_careers/manage_applications.html', context)

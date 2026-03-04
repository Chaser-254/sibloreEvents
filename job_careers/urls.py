from django.urls import path
from . import views

app_name = 'job_careers'

urlpatterns = [
    path('', views.career_list, name='list'),
    path('job/<slug:slug>/', views.career_detail, name='detail'),
    path('apply/<slug:slug>/', views.apply_job, name='apply'),
    path('application-success/', views.application_success, name='success'),
    path('manage-applications/', views.manage_applications, name='manage_applications'),
]

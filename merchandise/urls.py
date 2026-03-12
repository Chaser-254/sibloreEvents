from django.urls import path
from . import views

app_name = 'merchandise'

urlpatterns = [
    path('', views.MerchandiseListView.as_view(), name='list'),
    path('create/', views.MerchandiseCreateView.as_view(), name='create'),
    path('my-merchandise/', views.MyMerchandiseView.as_view(), name='my_merchandise'),
    path('<int:pk>/', views.MerchandiseDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.MerchandiseUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.MerchandiseDeleteView.as_view(), name='delete'),
]

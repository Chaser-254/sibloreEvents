from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('my-products/', views.MyProductsView.as_view(), name='my_products'),
    path('affiliate/', views.AffiliateDashboardView.as_view(), name='affiliate_dashboard'),
    path('create-affiliate-link/', views.CreateAffiliateLinkView.as_view(), name='create_affiliate_link'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
]

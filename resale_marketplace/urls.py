from django.urls import path
from . import views

app_name = 'resale_marketplace'

urlpatterns = [
    # Public views
    path('', views.ResaleMarketplaceView.as_view(), name='marketplace'),
    path('listing/<int:pk>/', views.ResaleListingDetailView.as_view(), name='listing_detail'),
    path('search/', views.search_listings, name='search'),
    
    # User views (require login)
    path('create/', views.CreateResaleListingView.as_view(), name='create_listing'),
    path('my-listings/', views.MyResaleListingsView.as_view(), name='my_listings'),
    path('my-purchases/', views.MyPurchasesView.as_view(), name='my_purchases'),
    path('purchase/<int:pk>/', views.purchase_ticket, name='purchase_ticket'),
    path('complete/<str:transaction_id>/', views.complete_purchase, name='complete_purchase'),
    path('transaction/<str:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('cancel/<int:pk>/', views.CancelListingView.as_view(), name='cancel_listing'),
    
    # Download views (require login)
    path('download/receipt/<str:transaction_id>/', views.download_receipt, name='download_receipt'),
    path('download/ticket/<str:transaction_id>/', views.download_ticket, name='download_ticket'),
    
    # Admin/staff verification views
    path('verification/queue/', views.VerificationQueueView.as_view(), name='verification_queue'),
    path('verification/verify/<int:pk>/', views.verify_ticket, name='verify_ticket'),
    path('verification/reject/<int:pk>/', views.reject_ticket, name='reject_ticket'),
]

from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('my-tickets/', views.MyTicketsView.as_view(), name='my_tickets'),
    path('purchase/<int:event_id>/', views.TicketPurchaseView.as_view(), name='purchase'),
    path('print/<uuid:ticket_id>/', views.TicketPrintView.as_view(), name='print'),
    path('<uuid:ticket_id>/', views.TicketDetailView.as_view(), name='detail'),
]

from django.urls import path
from .views import (
    InvoiceListCreateView,
    InvoiceDetailView,
    InvoiceStatusUpdateView,
    InvoicePDFView
)

urlpatterns = [
    path('', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('<int:pk>/status/', InvoiceStatusUpdateView.as_view(), name='invoice-status-update'),
    path('<int:pk>/pdf/', InvoicePDFView.as_view(), name='invoice-pdf'),
]
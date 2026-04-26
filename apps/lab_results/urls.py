from django.urls import path
from .views import LabResultListCreateView, LabResultDetailView

urlpatterns = [
    path('', LabResultListCreateView.as_view(), name='lab-result-list-create'),
    path('<int:pk>/', LabResultDetailView.as_view(), name='lab-result-detail'),
]
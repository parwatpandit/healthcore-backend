from django.urls import path
from .views import DiseasePredictionView, SymptomsListView

urlpatterns = [
    path('predict/', DiseasePredictionView.as_view(), name='disease-predict'),
    path('symptoms/', SymptomsListView.as_view(), name='symptoms-list'),
]
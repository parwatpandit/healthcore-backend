from django.urls import path
from .views import (
    AppointmentListCreateView,
    AppointmentDetailView,
    AppointmentStatusUpdateView,
    SendAppointmentRemindersView,
    SendSingleReminderView,
)

urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<int:pk>/status/', AppointmentStatusUpdateView.as_view(), name='appointment-status-update'),
    path('reminders/send-all/', SendAppointmentRemindersView.as_view(), name='send-all-reminders'),
    path('<int:pk>/reminder/', SendSingleReminderView.as_view(), name='send-single-reminder'),
]
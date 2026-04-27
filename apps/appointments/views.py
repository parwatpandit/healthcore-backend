from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentStatusSerializer
from .tasks import send_appointment_reminders, send_single_appointment_reminder


class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Appointment.objects.all()
        patient_id = self.request.query_params.get('patient')
        doctor_id = self.request.query_params.get('doctor')
        status_filter = self.request.query_params.get('status')
        date_filter = self.request.query_params.get('date')

        if patient_id:
            queryset = queryset.filter(patient__id=patient_id)
        if doctor_id:
            queryset = queryset.filter(doctor__id=doctor_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if date_filter:
            queryset = queryset.filter(appointment_date=date_filter)

        return queryset


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


class AppointmentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentStatusSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendAppointmentRemindersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task = send_appointment_reminders.delay()
        return Response({
            'message': 'Reminder task triggered successfully',
            'task_id': task.id
        }, status=status.HTTP_200_OK)


class SendSingleReminderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        task = send_single_appointment_reminder.delay(appointment.id)
        return Response({
            'message': f'Reminder triggered for appointment {pk}',
            'task_id': task.id
        }, status=status.HTTP_200_OK)
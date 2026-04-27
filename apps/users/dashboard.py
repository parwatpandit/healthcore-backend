from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.appointments.models import Appointment
from apps.billing.models import Invoice


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        # Core stats
        total_patients = Patient.objects.count()
        total_doctors = Doctor.objects.count()
        appointments_today = Appointment.objects.filter(
            appointment_date=today
        ).count()
        total_revenue = sum(
            inv.total_amount for inv in Invoice.objects.filter(status='paid')
        )

        # Appointments last 7 days
        last_7_days = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            count = Appointment.objects.filter(appointment_date=day).count()
            last_7_days.append({
                'date': day.strftime('%d %b'),
                'count': count
            })

        # Appointment status breakdown
        status_breakdown = []
        for status_choice in ['scheduled', 'completed', 'cancelled', 'no_show']:
            count = Appointment.objects.filter(status=status_choice).count()
            status_breakdown.append({
                'status': status_choice,
                'count': count
            })

        # Revenue last 6 months
        revenue_trend = []
        for i in range(5, -1, -1):
            month = today.replace(day=1) - timedelta(days=i * 30)
            month_invoices = Invoice.objects.filter(
                status='paid',
                issue_date__year=month.year,
                issue_date__month=month.month
            )
            total = sum(inv.total_amount for inv in month_invoices)
            revenue_trend.append({
                'month': month.strftime('%b %Y'),
                'revenue': float(total)
            })

        # Recent appointments
        recent_appointments = []
        for appt in Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:5]:
            patient = appt.patient
            patient_name = f'{patient.first_name} {patient.last_name}'.strip() or patient.user.username
            recent_appointments.append({
                'id': appt.id,
                'patient_name': patient_name,
                'doctor_name': appt.doctor.user.username,
                'date': appt.appointment_date,
                'time': appt.appointment_time,
                'status': appt.status,
            })

        # Recent invoices
        recent_invoices = []
        for inv in Invoice.objects.select_related('patient', 'doctor').order_by('-created_at')[:5]:
            patient = inv.patient
            patient_name = f'{patient.first_name} {patient.last_name}'.strip()
            recent_invoices.append({
                'id': inv.id,
                'invoice_number': inv.invoice_number,
                'patient_name': patient_name,
                'total_amount': float(inv.total_amount),
                'status': inv.status,
                'issue_date': inv.issue_date,
            })

        return Response({
            'stats': {
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'appointments_today': appointments_today,
                'total_revenue': float(total_revenue),
            },
            'appointments_last_7_days': last_7_days,
            'status_breakdown': status_breakdown,
            'revenue_trend': revenue_trend,
            'recent_appointments': recent_appointments,
            'recent_invoices': recent_invoices,
        })
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Appointment


@shared_task(name='send_appointment_reminders')
def send_appointment_reminders():
    tomorrow = timezone.now().date() + timedelta(days=1)
    appointments = Appointment.objects.filter(
        appointment_date=tomorrow,
        status='scheduled'
    ).select_related('patient', 'doctor')

    sent_count = 0

    for appointment in appointments:
        patient = appointment.patient
        doctor = appointment.doctor

        patient_email = patient.user.email
        patient_name = f'{patient.first_name} {patient.last_name}'.strip() or patient.user.username
        doctor_name = doctor.user.username
        specialisation = doctor.specialisation
        appt_date = appointment.appointment_date
        appt_time = appointment.appointment_time
        reason = appointment.reason or 'General Consultation'

        subject = f'Appointment Reminder — {appt_date} at {appt_time}'

        message = f"""
Dear {patient_name},

This is a reminder that you have an upcoming appointment at HealthCore.

Appointment Details:
———————————————————
Doctor      : {doctor_name}
Specialisation : {specialisation}
Date        : {appt_date}
Time        : {appt_time}
Reason      : {reason}
———————————————————

Please arrive 10 minutes before your scheduled time.
If you need to cancel or reschedule, please contact us as soon as possible.

Best regards,
HealthCore Hospital Management
        """.strip()

        send_mail(
            subject=subject,
            message=message,
            from_email='HealthCore <noreply@healthcore.com>',
            recipient_list=[patient_email],
            fail_silently=False,
        )
        sent_count += 1

    return f'{sent_count} reminder(s) sent for {tomorrow}'


@shared_task(name='send_single_appointment_reminder')
def send_single_appointment_reminder(appointment_id):
    try:
        appointment = Appointment.objects.select_related(
            'patient', 'doctor'
        ).get(id=appointment_id)
    except Appointment.DoesNotExist:
        return f'Appointment {appointment_id} not found'

    patient = appointment.patient
    doctor = appointment.doctor

    patient_email = patient.user.email
    patient_name = f'{patient.first_name} {patient.last_name}'.strip() or patient.user.username
    doctor_name = doctor.user.username
    specialisation = doctor.specialisation
    appt_date = appointment.appointment_date
    appt_time = appointment.appointment_time
    reason = appointment.reason or 'General Consultation'

    subject = f'Appointment Reminder — {appt_date} at {appt_time}'

    message = f"""
Dear {patient_name},

This is a reminder that you have an upcoming appointment at HealthCore.

Appointment Details:
———————————————————
Doctor      : {doctor_name}
Specialisation : {specialisation}
Date        : {appt_date}
Time        : {appt_time}
Reason      : {reason}
———————————————————

Please arrive 10 minutes before your scheduled time.
If you need to cancel or reschedule, please contact us as soon as possible.

Best regards,
HealthCore Hospital Management
    """.strip()

    send_mail(
        subject=subject,
        message=message,
        from_email='HealthCore <noreply@healthcore.com>',
        recipient_list=[patient_email],
        fail_silently=False,
    )

    return f'Reminder sent to {patient_email} for appointment {appointment_id}'
from django.db import models
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.appointments.models import Appointment


def lab_result_upload_path(instance, filename):
    return f'lab_results/patient_{instance.patient.id}/{filename}'


class LabResult(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('reviewed', 'Reviewed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='lab_results')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_results')
    test_name = models.CharField(max_length=255)
    test_date = models.DateField()
    result_file = models.FileField(upload_to=lab_result_upload_path, null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.test_name} for {self.patient}"
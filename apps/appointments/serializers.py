from rest_framework import serializers
from .models import Appointment
from apps.patients.serializers import PatientSerializer
from apps.doctors.serializers import DoctorSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'doctor',
            'patient_detail',
            'doctor_detail',
            'appointment_date',
            'appointment_time',
            'status',
            'reason',
            'notes',
            'created_at',
        ]
        extra_kwargs = {
            'patient': {'write_only': True},
            'doctor': {'write_only': True},
        }

    def validate(self, data):
        from django.utils import timezone
        if data.get('appointment_date') and data['appointment_date'] < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return data


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'status']

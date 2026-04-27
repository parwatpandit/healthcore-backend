from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'doctor',
            'patient_name',
            'doctor_name',
            'appointment_date',
            'appointment_time',
            'status',
            'reason',
            'notes',
            'created_at',
        ]
        extra_kwargs = {
            'patient': {'write_only': False},
            'doctor': {'write_only': False},
        }

    def get_patient_name(self, obj):
        first = obj.patient.first_name
        last = obj.patient.last_name
        if first and last:
            return f'{first} {last}'
        return obj.patient.user.username

    def get_doctor_name(self, obj):
        return obj.doctor.user.username

    def validate(self, data):
        from django.utils import timezone
        if data.get('appointment_date') and data['appointment_date'] < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return data


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'status']
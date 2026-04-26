from rest_framework import serializers
from .models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = [
            'id', 'patient', 'doctor', 'appointment',
            'medication_name', 'dosage', 'frequency', 'duration',
            'instructions', 'prescribed_date', 'is_active',
            'created_at', 'patient_name', 'doctor_name'
        ]

    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}".strip() or f"Patient {obj.patient.id}"
   
    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}".strip() or f"Doctor {obj.doctor.id}"
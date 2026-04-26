from rest_framework import serializers
from .models import LabResult


class LabResultSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    result_file_url = serializers.SerializerMethodField()

    class Meta:
        model = LabResult
        fields = [
            'id', 'patient', 'doctor', 'appointment',
            'test_name', 'test_date', 'result_file', 'result_file_url',
            'notes', 'status', 'created_at', 'patient_name', 'doctor_name'
        ]

    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}".strip() or f"Patient {obj.patient.id}"

    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}".strip() or f"Doctor {obj.doctor.id}"

    def get_result_file_url(self, obj):
        request = self.context.get('request')
        if obj.result_file and request:
            return request.build_absolute_uri(obj.result_file.url)
        return None
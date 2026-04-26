from rest_framework import generics, permissions
from .models import Prescription
from .serializers import PrescriptionSerializer


class PrescriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Prescription.objects.all()
        patient = self.request.query_params.get('patient')
        doctor = self.request.query_params.get('doctor')
        is_active = self.request.query_params.get('is_active')

        if patient:
            queryset = queryset.filter(patient_id=patient)
        if doctor:
            queryset = queryset.filter(doctor_id=doctor)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset


class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Prescription.objects.all()
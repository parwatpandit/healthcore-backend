from rest_framework import generics, permissions
from .models import LabResult
from .serializers import LabResultSerializer


class LabResultListCreateView(generics.ListCreateAPIView):
    serializer_class = LabResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = LabResult.objects.all()
        patient = self.request.query_params.get('patient')
        doctor = self.request.query_params.get('doctor')
        status = self.request.query_params.get('status')

        if patient:
            queryset = queryset.filter(patient_id=patient)
        if doctor:
            queryset = queryset.filter(doctor_id=doctor)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_serializer_context(self):
        return {'request': self.request}


class LabResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LabResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = LabResult.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}
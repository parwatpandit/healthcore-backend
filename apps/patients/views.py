from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Patient
from .serializers import PatientSerializer, PatientCreateSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatientCreateSerializer
        return PatientSerializer

    def get_queryset(self):
        queryset = Patient.objects.all()
        search = self.request.query_params.get('search')
        if search:
            parts = search.split()
            if len(parts) >= 2:
                queryset = queryset.filter(
                    Q(first_name__icontains=parts[0]) & Q(last_name__icontains=parts[-1])
                )
            else:
                queryset = queryset.filter(
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(user__email__icontains=search)
                )
        return queryset


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
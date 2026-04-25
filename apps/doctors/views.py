from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Doctor
from .serializers import DoctorSerializer, DoctorCreateSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DoctorCreateSerializer
        return DoctorSerializer

    def get_queryset(self):
        queryset = Doctor.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(specialisation__icontains=search) |
                Q(license_number__icontains=search) |
                Q(user__email__icontains=search)
            )
        return queryset


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
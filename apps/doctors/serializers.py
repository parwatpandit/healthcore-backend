from rest_framework import serializers
from apps.users.models import User
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'username',
            'email',
            'specialisation',
            'license_number',
            'years_experience',
            'available_days',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class DoctorCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = [
            'username',
            'email',
            'password',
            'specialisation',
            'license_number',
            'years_experience',
            'available_days',
        ]

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='doctor'
        )

        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor
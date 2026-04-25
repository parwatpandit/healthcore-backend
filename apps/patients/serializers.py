from rest_framework import serializers
from apps.users.models import User
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'username',
            'email',
            'date_of_birth',
            'blood_type',
            'allergies',
            'emergency_contact_name',
            'emergency_contact_phone',
            'medical_history',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PatientCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = [
            'username',
            'email',
            'password',
            'date_of_birth',
            'blood_type',
            'allergies',
            'emergency_contact_name',
            'emergency_contact_phone',
            'medical_history',
        ]

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='patient'
        )

        patient = Patient.objects.create(user=user, **validated_data)
        return patient
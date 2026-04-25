from django.db import models
from apps.users.models import User

class Doctor(models.Model):
    SPECIALISATION_CHOICES = [
        ('general', 'General Practice'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopaedics', 'Orthopaedics'),
        ('paediatrics', 'Paediatrics'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry'),
        ('oncology', 'Oncology'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
    ]

    AVAILABLE_DAYS_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialisation = models.CharField(max_length=20, choices=SPECIALISATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    years_experience = models.PositiveIntegerField(default=0)
    available_days = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialisation})"
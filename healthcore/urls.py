from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/patients/', include('apps.patients.urls')),
    path('api/doctors/', include('apps.doctors.urls')),
    path('api/appointments/', include('apps.appointments.urls')),
    path('api/prescriptions/', include('apps.prescriptions.urls')),
    path('api/lab-results/', include('apps.lab_results.urls')),
    path('api/billing/', include('apps.billing.urls')),
    path('api/ml/', include('apps.ml.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
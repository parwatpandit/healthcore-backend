from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    name = 'apps.appointments'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        import json

        try:
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute='0',
                hour='8',
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
            )

            PeriodicTask.objects.get_or_create(
                name='Send Daily Appointment Reminders',
                defaults={
                    'crontab': schedule,
                    'task': 'send_appointment_reminders',
                    'args': json.dumps([]),
                    'enabled': True,
                }
            )
        except Exception:
            pass
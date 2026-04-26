from django.db import models
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.appointments.models import Appointment


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='invoices')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')

    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last = Invoice.objects.order_by('id').last()
            next_id = (last.id + 1) if last else 1
            self.invoice_number = f'INV-{next_id:04d}'
        super().save(*args, **kwargs)

    @property
    def total_amount(self):
        return sum(item.line_total for item in self.items.all())

    def __str__(self):
        return f'{self.invoice_number} — {self.patient}'


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f'{self.description} x{self.quantity}'
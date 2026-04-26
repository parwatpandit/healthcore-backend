from rest_framework import serializers
from .models import Invoice, InvoiceItem
from apps.patients.models import Patient
from apps.doctors.models import Doctor


class InvoiceItemSerializer(serializers.ModelSerializer):
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'quantity', 'unit_price', 'line_total']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    total_amount = serializers.ReadOnlyField()

    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'status',
            'patient', 'patient_name',
            'doctor', 'doctor_name',
            'appointment', 'issue_date', 'due_date',
            'notes', 'items', 'total_amount', 'created_at'
        ]
        read_only_fields = ['invoice_number', 'issue_date', 'created_at']

    def get_patient_name(self, obj):
        return f'{obj.patient.first_name} {obj.patient.last_name}'

    def get_doctor_name(self, obj):
        return f'{obj.doctor.user.username} — {obj.doctor.specialisation}'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                InvoiceItem.objects.create(invoice=instance, **item)

        return instance
    
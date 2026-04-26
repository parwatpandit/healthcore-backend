from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Invoice.objects.all().order_by('-created_at')

        patient = self.request.query_params.get('patient')
        doctor = self.request.query_params.get('doctor')
        status_param = self.request.query_params.get('status')

        if patient:
            queryset = queryset.filter(patient__id=patient)
        if doctor:
            queryset = queryset.filter(doctor__id=doctor)
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()


class InvoiceStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        valid_statuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled']

        if not new_status:
            return Response({'error': 'status field is required'}, status=status.HTTP_400_BAD_REQUEST)
        if new_status not in valid_statuses:
            return Response({'error': f'Invalid status. Choose from {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)

        invoice.status = new_status
        invoice.save()
        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_200_OK)


class InvoicePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        context = {
            'invoice': invoice,
            'items': invoice.items.all(),
            'total_amount': invoice.total_amount,
            'patient_name': f'{invoice.patient.first_name} {invoice.patient.last_name}',
            'doctor_name': invoice.doctor.user.username,
            'doctor_specialisation': invoice.doctor.specialisation,
        }

        html_string = render_to_string('billing/invoice.html', context)
        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
        return response
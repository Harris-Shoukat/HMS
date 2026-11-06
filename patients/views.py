from datetime import timedelta

from django.utils import timezone
from rest_framework import generics

from .models import Patient
from .serializers import PatientSerializer


class UninsuredRecentAppointmentPatientsView(generics.ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        now = timezone.now()
        past_month = now - timedelta(days=30)

        return (
            Patient.objects.filter(
                insurance__isnull=True,
                appointments__appointment_date__gte=past_month,
                appointments__appointment_date__lte=now,
            )
            .distinct()
            .order_by("patient_id")
        )

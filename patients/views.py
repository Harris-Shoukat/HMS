from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import generics

from .models import Insurance, Patient
from .serializers import InsuranceProviderSerializer, PatientSerializer


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


class InsuranceProvidersView(generics.ListAPIView):
    serializer_class = InsuranceProviderSerializer

    def get_queryset(self):
        return (
            Insurance.objects
            .values("provider",)
            .annotate(active_patient_count=Count("patient_id"))
            .filter(active_patient_count__gt=0)
            .order_by("provider")
            .distinct()
        )

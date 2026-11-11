from datetime import timedelta

from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Insurance, Patient
from .serializers import (
    InsuranceProviderSerializer,
    PatientPrescriptionSerializer,
    PatientSerializer,
)


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


class RecentAppointmentPatientsWithPrescriptionsView(generics.ListAPIView):
    serializer_class = PatientPrescriptionSerializer

    def get_queryset(self):
        now = timezone.now()
        past_month = now - timedelta(days=30)

        return (
            Patient.objects.filter(
                appointments__appointment_date__gte=past_month,
                appointments__appointment_date__lte=now,
                prescriptions__isnull=False,
            )
            .distinct()
            .order_by("-appointments__appointment_date")
        )


class AverageAgeSurgeryPatientsWithoutAppointmentsView(APIView):
    def get(self, request):
        today = timezone.localdate()
        patients = Patient.objects.filter(
            surgeries__isnull=False,
            appointments__isnull=True,
        ).distinct()

        ages = [
            today.year - patient.dob.year
            - ((today.month, today.day) < (patient.dob.month, patient.dob.day))
            for patient in patients
        ]
        average_age = round(sum(ages) / len(ages), 2) if ages else None

        return Response({"average_age": average_age})

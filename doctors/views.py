from datetime import timedelta

from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics

from .models import Doctor, Surgery
from .serializers import DoctorSerializer, SurgeryCostSerializer


class HighlyBookedDoctorsView(generics.ListAPIView):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        now = timezone.now()
        six_months_ago = now - timedelta(days=180)

        return (
            Doctor.objects.annotate(
                appointment_count=Count(
                    "appointments",
                    filter=Q(appointments__appointment_date__gte=six_months_ago)
                    & Q(appointments__appointment_date__lte=now),
                )
            )
            .filter(appointment_count__gt=10)
            .order_by("doctor_id")
        )


class PatientSurgeryCostView(generics.ListAPIView):
    serializer_class = SurgeryCostSerializer

    def get_queryset(self):
        return (
            Surgery.objects
            .values("patient_id", "patient__name")
            .annotate(
                num_surgeries=models.Count("surgery_id"),
                total_cost=models.Sum("cost"),
            )
            .filter(num_surgeries__gt=1)
            .order_by("patient_id")
        )

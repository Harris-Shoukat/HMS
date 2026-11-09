from datetime import timedelta

from django.db import models
from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department, Doctor, Surgery
from .serializers import (
    DepartmentWithoutHeadSerializer,
    DoctorSerializer,
    SurgeryCostSerializer,
    UninsuredRecentSurgeryTotalSerializer,
)


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


class DepartmentsWithoutHeadDoctorView(generics.ListAPIView):
    serializer_class = DepartmentWithoutHeadSerializer

    def get_queryset(self):
        return (
            Department.objects.annotate(doctor_count=Count("doctors"))
            .filter(doctor_count__gte=3, head_doctor__isnull=True)
            .order_by("name")
        )


class UninsuredRecentSurgeryTotalView(APIView):
    serializer_class = UninsuredRecentSurgeryTotalSerializer

    def get(self, request):
        now = timezone.now()
        last_month = now - timedelta(days=30)

        total_billed = (
            Surgery.objects.filter(
                surgery_date__gte=last_month,
                surgery_date__lte=now,
                patient__insurance__isnull=True,
            ).aggregate(total_billed=Sum("cost"))["total_billed"]
        )

        payload = {"total_billed": total_billed}
        serializer = self.serializer_class(payload)
        return Response(serializer.data)

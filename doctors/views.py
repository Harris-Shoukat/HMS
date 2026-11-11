from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.db.models import Count, F, Q, Sum, Value
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.models import Appointment
from .models import Department, Doctor, Surgery
from .serializers import (
    DepartmentWithoutHeadSerializer,
    DoctorSerializer,
    DoctorPrescriptionCountSerializer,
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


class DoctorsWithAtLeastFivePrescriptionsView(generics.ListAPIView):
    serializer_class = DoctorPrescriptionCountSerializer

    def get_queryset(self):
        return (
            Doctor.objects.values("doctor_id", doctor_name=F("name"))
            .annotate(prescription_count=Count("prescriptions"))
            .filter(prescription_count__gte=5)
            .order_by("doctor_id")
        )


class IncreaseDoctorFeesView(APIView):
    def post(self, request):
        now = timezone.now()
        last_year = now - timedelta(days=365)

        doctors = (
            Doctor.objects.annotate(
                annual_appointment_count=Count(
                    "appointments",
                    filter=Q(
                        appointments__appointment_date__gte=last_year,
                        appointments__appointment_date__lte=now,
                        appointments__status=Appointment.Status.COMPLETED,
                    ),
                )
            )
            .filter(annual_appointment_count__gt=20)
            .filter(
                Q(last_fee_increase_date__isnull=True)
                | Q(last_fee_increase_date__lte=last_year)
            )
        )

        updated_count = doctors.update(
            fee=F("fee") * Value(Decimal("1.15")),
            last_fee_increase_amount=F("fee") * Value(Decimal("0.15")),
            last_fee_increase_date=now,
        )

        return Response({"updated_doctors": updated_count})


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

from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment
from .serializers import AppointmentSerializer, BulkAppointmentCreateSerializer


class UpcomingAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        now = timezone.now()
        next_seven_days = now + timedelta(days=7)
        return (
            Appointment.objects.select_related("patient", "doctor")
            .filter(
                status=Appointment.Status.SCHEDULED,
                appointment_date__gte=now,
                appointment_date__lte=next_seven_days,
            )
            .order_by("appointment_date")
        )


class UpdateAppointmentPrioritiesView(APIView):
    def post(self, request):
        now = timezone.now()
        three_days_from_now = now + timedelta(days=3)
        ten_days_from_now = now + timedelta(days=10)
        scheduled = Appointment.objects.filter(status=Appointment.Status.SCHEDULED)

        high_count = scheduled.filter(
            appointment_date__gte=now,
            appointment_date__lte=three_days_from_now,
        ).exclude(priority=Appointment.Priority.HIGH).update(
            priority=Appointment.Priority.HIGH
        )
        medium_count = scheduled.filter(
            appointment_date__gt=three_days_from_now,
            appointment_date__lte=ten_days_from_now,
        ).exclude(priority=Appointment.Priority.MEDIUM).update(
            priority=Appointment.Priority.MEDIUM
        )
        low_count = scheduled.exclude(
            appointment_date__gte=now,
            appointment_date__lte=ten_days_from_now,
        ).exclude(priority=Appointment.Priority.LOW).update(
            priority=Appointment.Priority.LOW
        )

        return Response(
            {"updated_count": high_count + medium_count + low_count}
        )


class InsuranceProviderWeekdayAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        provider = self.request.query_params.get("provider")
        if not provider:
            raise ValidationError({"provider": "This query parameter is required."})

        return (
            Appointment.objects.select_related("patient", "doctor")
            .filter(patient__insurance__provider=provider)
            .exclude(appointment_date__week_day=1)
            .order_by("appointment_date")
        )


class BulkCreateAppointmentsView(APIView):
    def post(self, request):
        serializer = BulkAppointmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        doctor = serializer.validated_data["doctor"]
        appointment_date = serializer.validated_data["appointment_date"]
        notes = serializer.validated_data["notes"]
        now = timezone.now()

        patient_ids = set(
            Appointment.objects.filter(
                doctor=doctor,
                status=Appointment.Status.COMPLETED,
                appointment_date__lt=now,
            )
            .values_list("patient_id", flat=True)
            .distinct()
        )
        already_scheduled = set(
            Appointment.objects.filter(
                doctor=doctor,
                status=Appointment.Status.SCHEDULED,
                appointment_date__gte=now,
                patient_id__in=patient_ids,
            ).values_list("patient_id", flat=True)
        )

        appointments = [
            Appointment(
                patient_id=patient_id,
                doctor=doctor,
                appointment_date=appointment_date,
                priority=self.get_priority(appointment_date, now),
                notes=notes,
            )
            for patient_id in patient_ids - already_scheduled
        ]

        with transaction.atomic():
            Appointment.objects.bulk_create(appointments)

        return Response(
            {
                "created_count": len(appointments),
                "skipped_count": len(already_scheduled),
            }
        )

    @staticmethod
    def get_priority(appointment_date, now):
        if now <= appointment_date <= now + timedelta(days=3):
            return Appointment.Priority.HIGH
        if now < appointment_date <= now + timedelta(days=10):
            return Appointment.Priority.MEDIUM
        return Appointment.Priority.LOW

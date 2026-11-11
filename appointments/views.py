from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import generics
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

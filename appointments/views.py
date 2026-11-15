from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment
from .serializers import (
    AppointmentBulkCreateItemSerializer,
    AppointmentSerializer,
)


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
        input_serializer = AppointmentBulkCreateItemSerializer(
            data=request.data,
            many=True,
        )
        input_serializer.is_valid(raise_exception=True)

        appointments = [
            Appointment(**item)
            for item in input_serializer.validated_data
        ]

        with transaction.atomic():
            appointments = Appointment.objects.bulk_create(appointments)
            now = timezone.now()
            past_appointments = [
                appointment
                for appointment in appointments
                if appointment.appointment_date <= now
            ]
            for appointment in past_appointments:
                appointment.status = Appointment.Status.COMPLETED
            if past_appointments:
                Appointment.objects.bulk_update(past_appointments, ["status"])

        return Response(
            {
                "created_count": len(appointments),
                "completed_count": len(past_appointments),
                "appointments": AppointmentSerializer(
                    appointments,
                    many=True,
                ).data,
            },
            status=201,
        )

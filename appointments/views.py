from datetime import timedelta

from django.utils import timezone
from rest_framework import generics

from .models import Appointment
from .serializers import AppointmentSerializer


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

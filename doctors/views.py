from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics

from .models import Doctor
from .serializers import DoctorSerializer


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

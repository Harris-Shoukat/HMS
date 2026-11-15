import calendar
from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

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


def _three_months_before(moment):
    month = moment.month - 3
    year = moment.year
    if month <= 0:
        month += 12
        year -= 1
    day = min(moment.day, calendar.monthrange(year, month)[1])
    return moment.replace(year=year, month=month, day=day)


class RecentSpecialtyRevenueView(APIView):
    def get(self, request):
        now = timezone.now()
        total_revenue = Appointment.objects.filter(
            status=Appointment.Status.COMPLETED,
            appointment_date__gte=_three_months_before(now),
            appointment_date__lte=now,
            doctor__specialization__in=("Cardiology", "Surgery"),
        ).aggregate(total=Sum("doctor__fee", default=Decimal("0.00")))["total"]

        return Response({"total_revenue": total_revenue})

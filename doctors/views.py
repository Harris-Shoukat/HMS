from django.db.models import Count
from rest_framework import generics

from .models import Doctor
from .serializers import DoctorAppointmentCountSerializer


class DoctorAppointmentCountListView(generics.ListAPIView):
	serializer_class = DoctorAppointmentCountSerializer

	def get_queryset(self):
		return (
			Doctor.objects.annotate(appointment_count=Count("appointments"))
			.prefetch_related("appointments")
			.order_by("doctor_id")
		)

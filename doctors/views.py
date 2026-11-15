from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics

from .models import Doctor
from .serializers import DoctorPatientCountSerializer


class DoctorsByRecentPatientCountView(generics.ListAPIView):
	serializer_class = DoctorPatientCountSerializer

	def get_queryset(self):
		now = timezone.now()
		one_year_ago = now - timedelta(days=365)
		return (
			Doctor.objects.annotate(
				patient_count=Count(
					"appointments__patient_id",
					distinct=True,
					filter=Q(
						appointments__appointment_date__gte=one_year_ago,
						appointments__appointment_date__lte=now,
					),
				)
			)
			.filter(patient_count__gt=5, patient_count__lt=15)
			.order_by("doctor_id")
		)

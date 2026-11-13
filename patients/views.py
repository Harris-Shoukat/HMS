from django.db.models import Count
from rest_framework import generics

from .models import Patient
from .serializers import PatientWithDoctorsSerializer


class PatientsWithMultipleDoctorsWithoutInsuranceView(generics.ListAPIView):
	serializer_class = PatientWithDoctorsSerializer

	def get_queryset(self):
		return (
			Patient.objects.annotate(doctor_count=Count("doctors", distinct=True))
			.filter(doctor_count__gt=1, insurance__isnull=True)
			.prefetch_related("doctors")
			.order_by("patient_id")
		)

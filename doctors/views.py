from django.db.models import Count
from rest_framework import generics

from .models import Doctor
from .serializers import SpecializationCountSerializer


class SpecializationListView(generics.ListAPIView):
	serializer_class = SpecializationCountSerializer

	def get_queryset(self):
		return (
			Doctor.objects.values("specialization")
			.annotate(doctor_count=Count("doctor_id"))
			.order_by("-doctor_count", "specialization")
		)

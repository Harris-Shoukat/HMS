from django.db.models import Q
from rest_framework import generics

from .models import Patient
from .serializers import InsuredSurgeryPatientSerializer


class InsuredSurgeryPatientListView(generics.ListAPIView):
	serializer_class = InsuredSurgeryPatientSerializer

	def get_queryset(self):
		return (
			Patient.objects.select_related("insurance")
			.filter(
				Q(insurance__isnull=False) & Q(surgeries__isnull=False)
			)
			.distinct()
			.order_by("patient_id")
		)

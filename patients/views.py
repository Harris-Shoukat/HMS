from rest_framework import generics

from .models import Patient
from .serializers import PatientSerializer


class PainkillerPrescriptionPatientListView(generics.ListAPIView):
	serializer_class = PatientSerializer

	def get_queryset(self):
		return Patient.objects.filter(
			prescriptions__medicine_details__icontains="Painkiller"
		).distinct().order_by("patient_id")

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient
from .serializers import PatientSerializer


class PatientsWithAppointmentsOrSurgeriesView(APIView):
	def get(self, request):
		patients = Patient.objects.filter(
			Q(appointments__isnull=False) | Q(surgeries__isnull=False)
		).distinct().order_by("patient_id")
		serializer = PatientSerializer(patients, many=True)
		return Response(serializer.data)

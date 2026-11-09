from rest_framework import serializers
from appointments.serializers import AppointmentSerializer
from .models import Insurance, Patient


class PatientSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = (
            "patient_id",
            "name",
            "dob",
            "gender",
            "address",
            "phone",
            "email",
            "appointments",
        )


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = ("provider",)

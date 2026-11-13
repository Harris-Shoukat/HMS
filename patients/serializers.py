from rest_framework import serializers

from doctors.models import Doctor
from .models import Patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "doctor_id",
            "name",
            "specialization",
            "phone",
            "email",
            "department",
        )


class PatientWithDoctorsSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(many=True, read_only=True)

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
            "doctors",
        )

from rest_framework import serializers

from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment


class PatientDetailsSerializer(serializers.ModelSerializer):
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
        )


class DoctorDetailsSerializer(serializers.ModelSerializer):
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


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientDetailsSerializer(read_only=True)
    doctor = DoctorDetailsSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = (
            "appointment_id",
            "patient",
            "doctor",
            "appointment_date",
            "status",
            "notes",
        )

from rest_framework import serializers

from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment, Prescription


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
            "priority",
            "notes",
        )


class BulkAppointmentCreateSerializer(serializers.Serializer):
    doctor_id = serializers.PrimaryKeyRelatedField(
        source="doctor",
        queryset=Doctor.objects.all(),
    )
    appointment_date = serializers.DateTimeField()
    notes = serializers.CharField(required=False, allow_blank=True, default="")


class AppointmentPrescriptionSerializer(serializers.ModelSerializer):
    doctor = DoctorDetailsSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = (
            "appointment_id",
            "doctor",
            "appointment_date",
            "status",
            "priority",
            "notes",
        )


class PrescriptionSerializer(serializers.ModelSerializer):
    appointment = AppointmentPrescriptionSerializer(read_only=True)
    doctor = DoctorDetailsSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = (
            "prescription_id",
            "appointment",
            "doctor",
            "medicine_details",
            "instructions",
        )

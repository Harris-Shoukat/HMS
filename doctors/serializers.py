from rest_framework import serializers

from .models import Doctor


class DoctorAppointmentCountSerializer(serializers.ModelSerializer):
    appointment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Doctor
        fields = (
            "doctor_id",
            "name",
            "specialization",
            "appointment_count",
        )

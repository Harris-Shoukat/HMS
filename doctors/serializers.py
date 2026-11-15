from rest_framework import serializers

from .models import Doctor


class DoctorPatientCountSerializer(serializers.ModelSerializer):
    patient_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Doctor
        fields = (
            "doctor_id",
            "name",
            "specialization",
            "patient_count",
        )

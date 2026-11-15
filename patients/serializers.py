from rest_framework import serializers

from .models import Insurance, Patient


class InsuranceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = (
            "insurance_id",
            "provider",
            "policy_number",
            "coverage_details",
        )


class InsuredSurgeryPatientSerializer(serializers.ModelSerializer):
    insurance = InsuranceDetailsSerializer(read_only=True)

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
            "insurance",
        )
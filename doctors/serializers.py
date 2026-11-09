from rest_framework import serializers

from .models import Department, Doctor, Surgery


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


class DepartmentWithoutHeadSerializer(serializers.ModelSerializer):
    doctor_count = serializers.IntegerField()

    class Meta:
        model = Department
        fields = ("department_id", "name", "doctor_count")


class SurgeryCostSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField()
    patient_name = serializers.CharField(source="patient__name")
    num_surgeries = serializers.IntegerField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Surgery
        fields = ("patient_id", "patient_name", "num_surgeries", "total_cost")

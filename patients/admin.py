from django.contrib import admin
from .models import Insurance, Patient, PatientDoctor


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id",
        "name",
        "gender",
        "phone",
        "email",
    )
    search_fields = ("name", "email", "phone")


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ("insurance_id", "patient", "provider", "policy_number")
    search_fields = ("patient__name", "provider", "policy_number")


@admin.register(PatientDoctor)
class PatientDoctorAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "relationship_type")
    list_filter = ("relationship_type",)
    search_fields = ("patient__name", "doctor__name")

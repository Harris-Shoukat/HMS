
from django.contrib import admin
from .models import Department, Doctor, Surgery


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("department_id", "name", "head_doctor")
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "doctor_id",
        "name",
        "specialization",
        "department",
        "email",
    )
    search_fields = ("name", "email", "specialization")
    list_filter = ("department",)


@admin.register(Surgery)
class SurgeryAdmin(admin.ModelAdmin):
    list_display = (
        "surgery_id",
        "surgery_type",
        "patient",
        "doctor",
        "surgery_date",
        "cost",
    )
    list_filter = ("surgery_type", "surgery_date")
    search_fields = ("patient__name", "doctor__name", "surgery_type", "notes")

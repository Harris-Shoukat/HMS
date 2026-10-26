
from django.contrib import admin
from .models import Department, Doctor


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

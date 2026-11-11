from django.contrib import admin
from .models import Appointment, Prescription


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_id",
        "patient",
        "doctor",
        "appointment_date",
        "status",
        "priority",
    )
    list_filter = ("status", "priority", "appointment_date")
    search_fields = ("patient__name", "doctor__name", "notes")


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "prescription_id",
        "appointment",
        "patient",
        "doctor",
    )
    search_fields = (
        "patient__name",
        "doctor__name",
        "medicine_details",
    )

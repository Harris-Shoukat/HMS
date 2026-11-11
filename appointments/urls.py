from django.urls import path

from .views import BulkCreateAppointmentsView, UpcomingAppointmentListView

app_name = "appointments"

urlpatterns = [
    # Post request body example for bulk-create endpoint:
    # {
    #   "doctor_id": 3,
    #   "appointment_date": "2026-12-01T10:00:00Z",
    #   "notes": "Follow-up"
    # }
    path(
        "bulk-create/",
        BulkCreateAppointmentsView.as_view(),
        name="bulk-create-appointments",
    ),
    path(
        "upcoming/",
        UpcomingAppointmentListView.as_view(),
        name="upcoming-appointments",
    ),
]

from django.urls import path

from .views import (
    BulkCreateAppointmentsView,
    InsuranceProviderWeekdayAppointmentsView,
    UpcomingAppointmentListView,
    UpdateAppointmentPrioritiesView,
)

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
    path(
        "update-priorities/",
        UpdateAppointmentPrioritiesView.as_view(),
        name="update-appointment-priorities",
    ),
    path(
        "insurance-weekday/",
        InsuranceProviderWeekdayAppointmentsView.as_view(),
        name="insurance-provider-weekday-appointments",
    ),
]

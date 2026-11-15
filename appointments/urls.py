from django.urls import path

from .views import BulkCreateAppointmentsView, UpcomingAppointmentListView

app_name = "appointments"

urlpatterns = [
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

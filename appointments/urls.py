from django.urls import path

from .views import UpcomingAppointmentListView

app_name = "appointments"

urlpatterns = [
    path(
        "upcoming/",
        UpcomingAppointmentListView.as_view(),
        name="upcoming-appointments",
    ),
]

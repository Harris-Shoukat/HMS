from django.urls import path

from .views import UninsuredRecentAppointmentPatientsView

app_name = "patients"

urlpatterns = [
    path(
        "uninsured/",
        UninsuredRecentAppointmentPatientsView.as_view(),
        name="uninsured-recent-appointments",
    ),
]

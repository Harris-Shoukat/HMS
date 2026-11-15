from django.urls import path

from .views import DoctorAppointmentCountListView

app_name = "doctors"

urlpatterns = [
    path(
        "appointment-counts/",
        DoctorAppointmentCountListView.as_view(),
        name="appointment-counts",
    ),
]

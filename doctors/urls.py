from django.urls import path

from .views import DoctorsByRecentPatientCountView

app_name = "doctors"

urlpatterns = [
    path(
        "patient-counts/",
        DoctorsByRecentPatientCountView.as_view(),
        name="recent-patient-counts",
    ),
]

from django.urls import path

from .views import HighlyBookedDoctorsView, PatientSurgeryCostView

app_name = "doctors"

urlpatterns = [
    path(
        "top/",
        HighlyBookedDoctorsView.as_view(),
        name="highly-booked-doctors",
    ),
    path(
        "surgery-costs/",
        PatientSurgeryCostView.as_view(),
        name="patient-surgery-costs",
    ),
]

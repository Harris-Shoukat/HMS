from django.urls import path

from .views import PatientsWithMultipleDoctorsWithoutInsuranceView

app_name = "patients"

urlpatterns = [
    path(
        "with-multiple-doctors-without-insurance/",
        PatientsWithMultipleDoctorsWithoutInsuranceView.as_view(),
        name="with-multiple-doctors-without-insurance",
    ),
]

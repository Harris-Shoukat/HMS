from django.urls import path

from .views import PainkillerPrescriptionPatientListView

app_name = "patients"

urlpatterns = [
    path(
        "painkiller-prescriptions/",
        PainkillerPrescriptionPatientListView.as_view(),
        name="painkiller-prescription-patients",
    ),
]
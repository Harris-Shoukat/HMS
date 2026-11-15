from django.urls import path

from .views import InsuredSurgeryPatientListView

app_name = "patients"

urlpatterns = [
    path(
        "insured-with-surgery/",
        InsuredSurgeryPatientListView.as_view(),
        name="insured-with-surgery",
    ),
]
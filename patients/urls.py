from django.urls import path

from .views import InsuranceProvidersView, UninsuredRecentAppointmentPatientsView

app_name = "patients"

urlpatterns = [
    path(
        "uninsured/",
        UninsuredRecentAppointmentPatientsView.as_view(),
        name="uninsured-recent-appointments",
    ),
    path(
        "insurance-providers/",
        InsuranceProvidersView.as_view(),
        name="insurance-providers",
    ),
]

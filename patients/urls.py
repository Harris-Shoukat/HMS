from django.urls import path

from .views import (
    InsuranceProvidersView,
    RecentAppointmentPatientsWithPrescriptionsView,
    UninsuredRecentAppointmentPatientsView,
)

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
    path(
        "recent-prescriptions/",
        RecentAppointmentPatientsWithPrescriptionsView.as_view(),
        name="recent-appointment-patients-with-prescriptions",
    ),
]

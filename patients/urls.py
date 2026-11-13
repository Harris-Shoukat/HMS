from django.urls import path

from .views import (
	PatientsWithAppointmentsAndPrescriptionsView,
	PatientsWithAppointmentsOrSurgeriesView,
)

app_name = "patients"

urlpatterns = [
	path(
		"with-appointments-or-surgeries/",
		PatientsWithAppointmentsOrSurgeriesView.as_view(),
		name="with-appointments-or-surgeries",
	),
	path(
		"with-appointments-and-prescriptions/",
		PatientsWithAppointmentsAndPrescriptionsView.as_view(),
		name="with-appointments-and-prescriptions",
	),
]
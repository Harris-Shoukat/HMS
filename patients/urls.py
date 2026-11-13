from django.urls import path

from .views import PatientsWithAppointmentsOrSurgeriesView

app_name = "patients"

urlpatterns = [
	path(
		"with-appointments-or-surgeries/",
		PatientsWithAppointmentsOrSurgeriesView.as_view(),
		name="with-appointments-or-surgeries",
	),
]
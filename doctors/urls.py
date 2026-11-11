from django.urls import path

from .views import (
    DepartmentsWithoutHeadDoctorView,
    HighlyBookedDoctorsView,
    IncreaseDoctorFeesView,
    PatientSurgeryCostView,
    UninsuredRecentSurgeryTotalView,
)

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
    path(
        "departments-without-head/",
        DepartmentsWithoutHeadDoctorView.as_view(),
        name="departments-without-head-doctor",
    ),
    path(
        "increase-fees/",
        IncreaseDoctorFeesView.as_view(),
        name="increase-fees",
    ),
    path(
        "uninsured-last-month-billed/",
        UninsuredRecentSurgeryTotalView.as_view(),
        name="uninsured-last-month-billed",
    ),
]

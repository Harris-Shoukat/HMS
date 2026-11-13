from django.urls import path

from .views import DoctorsWithAtLeastFiveRecentSurgeriesView

app_name = "doctors"

urlpatterns = [
    path(
        "surgeries/at-least-five-in-past-year/",
        DoctorsWithAtLeastFiveRecentSurgeriesView.as_view(),
        name="doctors-with-five-recent-surgeries",
    ),
]
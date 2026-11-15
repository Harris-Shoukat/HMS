from django.urls import path

from .views import SpecializationListView

app_name = "doctors"

urlpatterns = [
    path(
        "specializations/",
        SpecializationListView.as_view(),
        name="specializations",
    ),
]

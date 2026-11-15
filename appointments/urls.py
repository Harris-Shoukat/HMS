from django.urls import path

from .views import RecentSpecialtyRevenueView, UpcomingAppointmentListView

app_name = "appointments"

urlpatterns = [
    path(
        "revenue/last-three-months/",
        RecentSpecialtyRevenueView.as_view(),
        name="recent-specialty-revenue",
    ),
    path(
        "upcoming/",
        UpcomingAppointmentListView.as_view(),
        name="upcoming-appointments",
    ),
]

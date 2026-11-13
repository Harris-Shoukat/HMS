from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Doctor


class DoctorsWithAtLeastFiveRecentSurgeriesView(APIView):
	def get(self, request):
		now = timezone.now()
		one_year_ago = now - timedelta(days=365)
		doctor_ids = list(
			Doctor.objects.annotate(
				recent_surgery_count=Count(
					"surgeries",
					filter=Q(
						surgeries__surgery_date__gte=one_year_ago,
						surgeries__surgery_date__lte=now,
					),
				)
			)
			.filter(recent_surgery_count__gte=5)
			.order_by("doctor_id")
			.values_list("doctor_id", flat=True)
		)
		return Response({"doctor_ids": doctor_ids})

from django.core.management.base import BaseCommand
from django.utils import timezone

from appointments.models import Appointment


class Command(BaseCommand):
    help = 'Mark past "Scheduled" appointments as "Missed".'

    def handle(self, *args, **options):
        updated_count = Appointment.objects.filter(
            status=Appointment.Status.SCHEDULED,
            appointment_date__lt=timezone.now(),
        ).update(status=Appointment.Status.MISSED)

        self.stdout.write(
            self.style.SUCCESS(
                f"Marked {updated_count} past scheduled appointment(s) as Missed."
            )
        )

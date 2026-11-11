from django.db import models


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "Scheduled", "Scheduled"
        COMPLETED = "Completed", "Completed"
        CANCELLED = "Cancelled", "Cancelled"
        MISSED = "Missed", "Missed"

    class Priority(models.TextChoices):
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    appointment_date = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date:%Y-%m-%d %H:%M}"


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.PROTECT,
        related_name="prescription",
    )
    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.PROTECT,
        related_name="prescriptions",
    )
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.PROTECT,
        related_name="prescriptions",
    )
    medicine_details = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return f"Prescription {self.prescription_id} for {self.patient}"

from django.db import models


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"
        OTHER = "Other", "Other"

    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    doctors = models.ManyToManyField(
        "doctors.Doctor",
        through="PatientDoctor",
        related_name="patients",
    )

    def __str__(self):
        return self.name


class Insurance(models.Model):
    insurance_id = models.AutoField(primary_key=True)
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="insurance",
    )
    provider = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=255)
    coverage_details = models.TextField()

    def __str__(self):
        return f"{self.provider} - {self.policy_number}"


class PatientDoctor(models.Model):
    class RelationshipType(models.TextChoices):
        PRIMARY_CARE = "Primary Care", "Primary Care"
        CONSULTATION = "Consultation", "Consultation"
        SPECIALIST = "Specialist", "Specialist"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="doctor_relationships",
    )
    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.CASCADE,
        related_name="patient_relationships",
    )
    relationship_type = models.CharField(
        max_length=20,
        choices=RelationshipType.choices,
    )

    class Meta:
        db_table = "Patient_Doctor"
        constraints = [
            models.UniqueConstraint(
                fields=("patient", "doctor"),
                name="unique_patient_doctor_relationship",
            ),
        ]

    def __str__(self):
        return f"{self.patient} - {self.doctor} ({self.relationship_type})"

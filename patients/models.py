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

    def __str__(self):
        return self.name

from decimal import Decimal

from django.test import TestCase

from doctors.models import Department, Doctor, Surgery
from patients.models import Patient


class SurgeryCostQueryTests(TestCase):
    def test_patient_totals_for_multiple_surgeries(self):
        department = Department.objects.create(name="Cardiology")
        doctor = Doctor.objects.create(
            name="Dr. Smith",
            specialization="Cardiologist",
            phone="1234567890",
            email="smith@example.com",
            department=department,
        )

        patient_a = Patient.objects.create(
            name="Alice",
            dob="1990-01-01",
            gender=Patient.Gender.FEMALE,
            address="123 Main St",
            phone="1111111111",
            email="alice@example.com",
        )
        patient_b = Patient.objects.create(
            name="Bob",
            dob="1985-02-02",
            gender=Patient.Gender.MALE,
            address="456 Side St",
            phone="2222222222",
            email="bob@example.com",
        )

        Surgery.objects.create(
            patient=patient_a,
            doctor=doctor,
            surgery_date="2026-01-01T10:00:00Z",
            surgery_type="Heart Valve Repair",
            cost=Decimal("250.50"),
        )
        Surgery.objects.create(
            patient=patient_a,
            doctor=doctor,
            surgery_date="2026-02-01T10:00:00Z",
            surgery_type="Coronary Bypass",
            cost=Decimal("450.75"),
        )
        Surgery.objects.create(
            patient=patient_b,
            doctor=doctor,
            surgery_date="2026-03-01T10:00:00Z",
            surgery_type="Appendectomy",
            cost=Decimal("300.00"),
        )

        result = list(
            Surgery.objects.patient_totals_for_multiple_surgeries()
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["patient_id"], patient_a.patient_id)
        self.assertEqual(result[0]["patient__name"], "Alice")
        self.assertEqual(result[0]["num_surgeries"], 2)
        self.assertEqual(result[0]["total_cost"], Decimal("701.25"))

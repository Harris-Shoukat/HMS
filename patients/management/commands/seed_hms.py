import random
from uuid import uuid4

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from faker import Faker

from appointments.models import Appointment, Prescription
from doctors.models import Department, Doctor, Surgery
from patients.models import Insurance, Patient, PatientDoctor


DEPARTMENT_SPECIALTIES = {
    "Cardiology": ["Cardiologist", "Cardiac Electrophysiologist"],
    "Orthopedics": ["Orthopedic Surgeon", "Sports Medicine Physician"],
    "Emergency Medicine": ["Emergency Medicine Physician"],
    "Neurology": ["Neurologist", "Neurosurgeon"],
    "Dermatology": ["Dermatologist"],
    "Pediatrics": ["Pediatrician", "Pediatric Cardiologist"],
    "Oncology": ["Medical Oncologist", "Radiation Oncologist"],
    "Radiology": ["Diagnostic Radiologist", "Interventional Radiologist"],
    "General Medicine": ["General Physician", "Internal Medicine Physician"],
    "Obstetrics and Gynecology": ["Obstetrician-Gynecologist"],
}
DOCTOR_NAMES = [
    "Dr. Ahmed Khan",
    "Dr. Ayesha Malik",
    "Dr. Muhammad Ali",
    "Dr. Fatima Hussain",
    "Dr. Usman Sheikh",
    "Dr. Sana Ahmed",
    "Dr. Bilal Raza",
    "Dr. Zainab Qureshi",
    "Dr. Hamza Siddiqui",
    "Dr. Maryam Iqbal",
]
PATIENT_NAMES = [
    "Ali Raza",
    "Sara Ahmed",
    "Moeen Shah",
    "Ayesha Khan",
    "Usman Malik",
    "Fatima Hussain",
    "Bilal Sheikh",
    "Zainab Qureshi",
    "Hamza Siddiqui",
    "Maryam Iqbal",
    "Hassan Abbas",
    "Noor Fatima",
    "Imran Akhtar",
    "Hira Javed",
    "Farhan Chaudhry",
    "Sana Tariq",
    "Adnan Mahmood",
    "Maham Yousaf",
    "Salman Butt",
    "Iqra Bashir",
    "Danish Nawaz",
    "Laiba Aslam",
    "Omar Farooq",
    "Mehwish Anwar",
    "Shahid Mirza",
    "Rabia Khalid",
    "Kamran Baig",
    "Sadia Noor",
    "Tariq Masood",
    "Nida Rehman",
    "Adeel Hussain",
    "Komal Siddiqui",
    "Faisal Iqbal",
    "Amina Zahid",
]


class Command(BaseCommand):
    help = "Populate the HMS database with realistic sample data."

    def add_arguments(self, parser):
        parser.add_argument("--departments", type=int, default=5)
        parser.add_argument("--doctors", type=int, default=10)
        parser.add_argument("--patients", type=int, default=30)
        parser.add_argument("--appointments", type=int, default=50)
        parser.add_argument("--prescriptions", type=int, default=20)
        parser.add_argument("--surgeries", type=int, default=10)
        parser.add_argument("--seed", type=int, help="Use a fixed random seed.")

    def handle(self, *args, **options):
        counts = {
            name: options[name]
            for name in (
                "departments",
                "doctors",
                "patients",
                "appointments",
                "prescriptions",
                "surgeries",
            )
        }
        if any(count < 0 for count in counts.values()):
            raise CommandError("Record counts must be zero or greater.")

        if counts["doctors"] and not counts["departments"]:
            raise CommandError("At least one department is needed to create doctors.")
        if any(counts[name] for name in ("appointments", "prescriptions", "surgeries")):
            if not counts["patients"] or not counts["doctors"]:
                raise CommandError(
                    "Appointments, prescriptions, and surgeries require patients and doctors."
                )
        if counts["prescriptions"] > counts["appointments"]:
            raise CommandError(
                "Prescription count cannot exceed appointment count; each appointment "
                "can have at most one prescription."
            )

        seed = options["seed"]
        if seed is not None:
            random.seed(seed)

        fake = Faker()
        if seed is not None:
            fake.seed_instance(seed)

        with transaction.atomic():
            department_names = list(DEPARTMENT_SPECIALTIES)
            while len(department_names) < counts["departments"]:
                department_names.append(
                    f"Specialty Department {len(department_names) + 1}"
                )
            departments = [
                Department.objects.create(name=department_names[index])
                for index in range(counts["departments"])
            ]

            doctors = []
            for doctor_index in range(counts["doctors"]):
                department = random.choice(departments)
                doctors.append(Doctor.objects.create(
                    name=DOCTOR_NAMES[doctor_index % len(DOCTOR_NAMES)],
                    specialization=random.choice(
                        DEPARTMENT_SPECIALTIES.get(
                            department.name, ["General Physician"]
                        )
                    ),
                    phone=fake.phone_number()[:15],
                    email=f"doctor-{uuid4().hex[:8]}@hms.example.com",
                    department=department,
                ))

            # Only assign a head from the doctors working in that department.
            for department in departments:
                department_doctor = next(
                    (
                        doctor
                        for doctor in doctors
                        if doctor.department_id == department.department_id
                    ),
                    None,
                )
                if department_doctor is not None:
                    department.head_doctor = department_doctor
                    department.save(update_fields=["head_doctor"])

            patients = []
            for patient_index in range(counts["patients"]):
                patient = Patient.objects.create(
                    name=PATIENT_NAMES[patient_index % len(PATIENT_NAMES)],
                    dob=fake.date_of_birth(minimum_age=1, maximum_age=100),
                    gender=random.choice(Patient.Gender.values),
                    address=fake.address(),
                    phone=fake.phone_number()[:15],
                    email=fake.email(),
                )
                patients.append(patient)

                if random.random() < 0.7:
                    Insurance.objects.create(
                        patient=patient,
                        provider=fake.company(),
                        policy_number=f"POL-{uuid4().hex[:12].upper()}",
                        coverage_details=fake.paragraph(),
                    )

                if doctors:
                    assigned_doctors = random.sample(
                        doctors, k=random.randint(1, min(3, len(doctors)))
                    )
                    for doctor in assigned_doctors:
                        PatientDoctor.objects.create(
                            patient=patient,
                            doctor=doctor,
                            relationship_type=random.choice(
                                PatientDoctor.RelationshipType.values
                            ),
                        )

            appointments = [
                Appointment.objects.create(
                    patient=random.choice(patients),
                    doctor=random.choice(doctors),
                    appointment_date=fake.date_time_between(
                        start_date="-1y",
                        end_date="+1y",
                        tzinfo=timezone.get_current_timezone(),
                    ),
                    status=random.choice(Appointment.Status.values),
                    notes=fake.sentence() if random.random() < 0.7 else "",
                )
                for _ in range(counts["appointments"])
            ]

            for appointment in random.sample(
                appointments, k=counts["prescriptions"]
            ):
                Prescription.objects.create(
                    appointment=appointment,
                    doctor=appointment.doctor,
                    patient=appointment.patient,
                    medicine_details=fake.sentence(),
                    instructions=fake.paragraph(),
                )

            for _ in range(counts["surgeries"]):
                Surgery.objects.create(
                    patient=random.choice(patients),
                    doctor=random.choice(doctors),
                    surgery_date=fake.date_time_between(
                        start_date="-1y",
                        end_date="+1y",
                        tzinfo=timezone.get_current_timezone(),
                    ),
                    surgery_type=fake.job(),
                    cost=round(random.uniform(250.00, 8500.00), 2),
                    notes=fake.sentence() if random.random() < 0.7 else "",
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Created sample HMS data: "
                f"{counts['departments']} departments, "
                f"{counts['doctors']} doctors, "
                f"{counts['patients']} patients, "
                f"{counts['appointments']} appointments, "
                f"{counts['prescriptions']} prescriptions, "
                f"{counts['surgeries']} surgeries."
            )
        )

### **Hospital Management System (HMS) - Requirement Notes**

- Database: PostgreSQL
- Database management tool: pgAdmin
- Project uses Django with PostgreSQL configured for the HMS application.

### **Hospital Management System (HMS) - Database Schema**

### **Tables and Relationships**

**Patients**

- `patient_id` (PK, INT, AUTO_INCREMENT)
- `name` (VARCHAR(255))
- `dob` (DATE)
- `gender` (ENUM('Male', 'Female', 'Other'))
- `address` (TEXT)
- `phone` (VARCHAR(15))
- `email` (VARCHAR(255))
- `insurance_id` (FK, INT, UNIQUE) → *One-to-One with Insurance*

**Relationships**

- One-to-One with Insurance
- One-to-Many with Appointments
- Many-to-Many with Doctors through Patient_Doctor
- One-to-Many with Surgeries
- One-to-Many with Prescriptions

**Doctors**

- `doctor_id` (PK, INT, AUTO_INCREMENT)
- `name` (VARCHAR(255))
- `specialization` (VARCHAR(255))
- `phone` (VARCHAR(15))
- `email` (VARCHAR(255))
- `department_id` (FK, INT) → *Many-to-One with Departments*

**Relationships**

- One-to-Many with Appointments
- One-to-Many with Prescriptions
- One-to-Many with Surgeries
- Many-to-Many with Patients through Patient_Doctor
- Many-to-One with Departments
- One-to-One with Departments as department head

**Departments**

- `department_id` (PK, INT, AUTO_INCREMENT)
- `name` (VARCHAR(255))
- `head_doctor_id` (FK, INT, UNIQUE) → *One-to-One with Doctor as department head*

**Relationships**

- One-to-Many with Doctors
- One-to-One with Doctor as department head

**Appointments**

- `appointment_id` (PK, INT, AUTO_INCREMENT)
- `patient_id` (FK, INT) → *Many-to-One with Patients*
- `doctor_id` (FK, INT) → *Many-to-One with Doctors*
- `appointment_date` (DATETIME)
- `status` (ENUM('Scheduled', 'Completed', 'Cancelled'))
- `notes` (TEXT)

**Relationships**

- Many-to-One with Patients
- Many-to-One with Doctors
- One-to-One with Prescriptions

**Prescriptions**

- `prescription_id` (PK, INT, AUTO_INCREMENT)
- `appointment_id` (FK, INT, UNIQUE) → *One-to-One with Appointments*
- `doctor_id` (FK, INT) → *Many-to-One with Doctors*
- `patient_id` (FK, INT) → *Many-to-One with Patients*
- `medicine_details` (TEXT)
- `instructions` (TEXT)

**Relationships**

- One-to-One with Appointments
- Many-to-One with Doctors
- Many-to-One with Patients

**Insurance**

- `insurance_id` (PK, INT, AUTO_INCREMENT)
- `patient_id` (FK, INT, UNIQUE) → *One-to-One with Patients*
- `provider` (VARCHAR(255))
- `policy_number` (VARCHAR(255))
- `coverage_details` (TEXT)

**Relationships**

- One-to-One with Patients

**Surgeries**

- `surgery_id` (PK, INT, AUTO_INCREMENT)
- `patient_id` (FK, INT) → *Many-to-One with Patients*
- `doctor_id` (FK, INT) → *Many-to-One with Doctors*
- `surgery_date` (DATETIME)
- `surgery_type` (VARCHAR(255))
- `notes` (TEXT)

**Relationships**

- Many-to-One with Patients
- Many-to-One with Doctors

**Patient_Doctor**

- `patient_id` (FK, INT) → *Many-to-Many between Patients and Doctors*
- `doctor_id` (FK, INT) → *Many-to-Many between Patients and Doctors*
- `relationship_type` (ENUM('Primary Care', 'Consultation', 'Specialist'))

**Relationships**

- Many-to-Many between Patients and Doctors
- Composite unique constraint on (patient_id, doctor_id) to prevent duplicate associations

### **Hospital Management System (HMS) - Progress Summary**

**Project Setup**

- Created a Django project using Python.
- Configured PostgreSQL as the database.
- Installed Django REST Framework.
- Configured database credentials using a `.env` file.
- Created and activated a Python virtual environment (`.venv`).

**Database Migrations**

- Applied Django's default migrations for authentication, admin, sessions, and content types.
- Verified the project using `python manage.py check`.
- Confirmed migrations are applied using `python manage.py showmigrations`.

**Django Admin**

- Created a superuser account.
- Set up Django Admin to manage HMS data.
- Started the development server using `python manage.py runserver`.

**Patients App**

- Created the `patients` app.
- Defined the `Patient` model with:
	- `patient_id` — Primary key
	- `name`
	- `dob`
	- `gender` — Male, Female, or Other
	- `address`
	- `phone`
	- `email`
- Configured the model for database migrations.
- Registered the Patient model in Django Admin.

**Doctors App**

- Created the `doctors` app and added it to `INSTALLED_APPS`.
- Defined the `Department` model with:
	- `department_id` — Primary key
	- `name`
	- `head_doctor` — One-to-one relationship with Doctor
- Defined the `Doctor` model with:
	- `doctor_id` — Primary key
	- `name`
	- `specialization`
	- `phone`
	- `email`
	- `department` — Foreign key to Department
- Configured deletion behavior and related names for model relationships.
- Registered both models in Django Admin.

**Appointments App**

- Defined the `Appointment` model with:
	- `appointment_id` — Primary key
	- `patient` — Foreign key to Patient
	- `doctor` — Foreign key to Doctor
	- `appointment_date`
	- `status` — Scheduled, Completed, or Cancelled
	- `notes` — Optional notes
- Registered Appointment in Django Admin.
- Patient and Doctor records are protected from deletion while appointments reference them.

**Insurance Model**

- Defined `Insurance` in the `patients` app with `insurance_id`, `patient`, `provider`, `policy_number`, and `coverage_details`.
- `patient` is a one-to-one relationship, so each patient can have at most one insurance record and each insurance record belongs to one patient.
- Deleting a patient also deletes their insurance record.
- Registered Insurance in Django Admin.

**Patient_Doctor Relationship**

- Added a many-to-many relationship between Patient and Doctor through the `PatientDoctor` model.
- The association stores `relationship_type` (Primary Care, Consultation, or Specialist).
- Added a unique constraint on `(patient, doctor)` to prevent duplicate links.
- Deleting a patient or doctor removes its association records.
- Registered the association model in Django Admin.

**Prescription and Surgery Models**

- Defined `Prescription` in the `appointments` app with a one-to-one relationship to Appointment and foreign keys to Patient and Doctor.
- Defined `Surgery` in the `doctors` app with foreign keys to Patient and Doctor, plus the surgery date, type, and notes.
- Registered both models in Django Admin.
- Configured protected relationships so referenced appointments, patients, and doctors cannot be deleted while these records exist.

**Current Status**

- Project setup and default migrations are complete.
- Patient, Doctor, Department, Appointment, Insurance, PatientDoctor, Prescription, and Surgery models have been written.
- Django Admin configuration has been prepared for managing the models.

**Next Steps**

1. Apply and verify the migrations for all HMS models.
2. Test model records and relationships in Django Admin.
3. Build REST APIs using Django REST Framework.

**Development Approach**

- Complete and test the database models and relationships before implementing the REST APIs.

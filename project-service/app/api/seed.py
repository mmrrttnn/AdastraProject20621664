from app.api.models import (
    HospitalCreate, DoctorCreate, PatientCreate, ReceiptCreate, AppointmentCreate
)
from app.api.db_manager import (
    add_hospital, add_doctor, add_patient, add_receipt, add_appointment
)

async def seed_data():
    # Hospitals
    hospitals_data = [
        HospitalCreate(hospital_name="Hospital A", hospital_address="123 Main St"),
        HospitalCreate(hospital_name="Hospital B", hospital_address="456 Elm St"),
    ]
    for hospital_data in hospitals_data:
        await add_hospital(hospital_data)

    # Doctors
    doctors_data = [
        DoctorCreate(
            doctor_name="Dr. Smith",
            doctor_specialisation="Cardiologist",
            doctor_phone_number="555-1234",
            hospital_id=1,  # Assuming Hospital A has id 1
        ),
        DoctorCreate(
            doctor_name="Dr. Johnson",
            doctor_specialisation="Pediatrician",
            doctor_phone_number="555-5678",
            hospital_id=2,  # Assuming Hospital B has id 2
        ),
    ]
    for doctor_data in doctors_data:
        await add_doctor(doctor_data)

    # Patients
    patients_data = [
        PatientCreate(patient_name="Alice", patient_number="P001"),
        PatientCreate(patient_name="Bob", patient_number="P002"),
    ]
    for patient_data in patients_data:
        await add_patient(patient_data)

    # Receipts
    receipts_data = [
        ReceiptCreate(receipt_text="Receipt for patient Alice"),
        ReceiptCreate(receipt_text="Receipt for patient Bob"),
    ]
    for receipt_data in receipts_data:
        await add_receipt(receipt_data)

    # Appointments
    appointments_data = [
        AppointmentCreate(
            appointment_date="2024-04-25",
            appointment_reason="Checkup",
            doctor_id=1,  # Dr. Smith
            patient_id=1,  # Alice
            receipt_id=1,  # Receipt for Alice
        ),
        AppointmentCreate(
            appointment_date="2024-04-26",
            appointment_reason="Vaccination",
            doctor_id=2,  # Dr. Johnson
            patient_id=2,  # Bob
            receipt_id=2,  # Receipt for Bob
        ),
    ]
    for appointment_data in appointments_data:
        await add_appointment(appointment_data)



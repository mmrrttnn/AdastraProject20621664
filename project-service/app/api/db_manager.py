from app.api.models import(
    HospitalCreate, HospitalOut, HospitalUpdate,
    DoctorCreate, DoctorOut, DoctorUpdate,
    PatientCreate, PatientOut, PatientUpdate,
    ReceiptCreate, ReceiptOut, ReceiptUpdate,
    AppointmentCreate, AppointmentOut, AppointmentUpdate
)

from app.api.db import (
    hospital, doctor, patient, receipt, appointment, database
)
async def add_hospital(payload: HospitalCreate):
    query = hospital.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_hospitals():
    query = hospital.select()
    results = await database.fetch_all(query=query)
    return [
        {
            field: result[field]
            for field in HospitalOut.__fields__.keys()
            if field in results
        }
        for result in results
    ]


async def get_hospital(id: int):
    query = hospital.select().where(hospital.c.hospital_id == id)
    result = await database.fetch_one(query=query)
    if result:
        return {
            field: result[field]
            for field in HospitalOut.__fields__.keys()
            if field in result
        }
    return result


async def delete_hospital(id: int):
    query = hospital.delete().where(hospital.c.hospital_id == id)
    return await database.execute(query=query)


async def update_hospital(id: int, payload: HospitalUpdate):
    query = hospital.update().where(hospital.c.hospital_id == id).values(**payload.dict())
    await database.execute(query=query)
    return await get_hospital(id)


'''async def add_doctor(payload: DoctorCreate):
    query = doctor.insert().values(**payload.dict())
    return await database.execute(query=query)'''
async def add_doctor(payload: DoctorCreate):
    query = doctor.insert().values(
        doctor_name=payload.doctor_name,
        doctor_specialisation=payload.doctor_specialization,
        doctor_phone_number=payload.doctor_phone_number,
        hospital_id=payload.hospital_id
    )
    return await database.execute(query=query)



async def get_all_doctors():
    query = doctor.select()
    results = await database.fetch_all(query=query)
    return [
        {
            field: result[field]
            for field in DoctorOut.__fields__.keys()
            if field in results
        }
        for result in results
    ]


async def get_doctor(id: int):
    query = doctor.select().where(doctor.c.doctor_id == id)
    result = await database.fetch_one(query=query)
    if result:
        return {
            field: result[field]
            for field in DoctorlOut.__fields__.keys()
            if field in result
        }
    return result


async def delete_doctor(id: int):
    query = doctor.delete().where(doctor.c.doctor_id == id)
    return await database.execute(query=query)


async def update_doctor(id: int, payload: DoctorUpdate):
    query = doctor.update().where(doctor.c.doctor_id == id).values(**payload.dict())
    await database.execute(query=query)
    return await get_doctor(id)


async def add_patient(payload: PatientCreate):
    query = patient.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_patients():
    query = patient.select()
    results = await database.fetch_all(query=query)
    return [
        {
            field: result[field]
            for field in PatientOut.__fields__.keys()
            if field in result
        }
        for result in results
    ]


async def get_patient(id: int):
    query = patient.select().where(patient.c.patient_id == id)
    result = await database.fetch_one(query=query)
    if result:
        return {
            field: result[field]
            for field in PatientOut.__fields__.keys()
            if field in result
        }
    return result


async def delete_patient(id: int):
    query = patient.delete().where(patient.c.patient_id == id)
    return await database.execute(query=query)


async def update_patient(id: int, payload: PatientUpdate):
    query = patient.update().where(patient.c.patient_id == id).values(**payload.dict())
    await database.execute(query=query)
    return await get_patient(id)


async def add_receipt(payload: ReceiptCreate):
    query = receipt.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_receipts():
    query = receipt.select()
    results = await database.fetch_all(query=query)
    return [
        {
            field: result[field]
            for field in ReceiptOut.__fields__.keys()
            if field in result
        }
        for result in results
    ]


async def get_receipt(id: int):
    query = receipt.select().where(receipt.c.receipt_id == id)
    result = await database.fetch_one(query=query)
    if result:
        return {
            field: result[field]
            for field in ReceiptOut.__fields__.keys()
            if field in result
        }
    return result


async def delete_receipt(id: int):
    query = receipt.delete().where(receipt.c.receipt_id == id)
    return await database.execute(query=query)


async def update_receipt(id: int, payload: ReceiptUpdate):
    query = receipt.update().where(receipt.c.receipt_id == id).values(**payload.dict())
    await database.execute(query=query)
    return await get_receipt(id)

async def add_appointment(payload: AppointmentCreate):
    query = appointment.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_appointments():
    query = appointment.select()
    results = await database.fetch_all(query=query)
    return [
        {
            field: result[field]
            for field in AppointmentOut.__fields__.keys()
            if field in result
        }
        for result in results
    ]


async def get_appointment(id: int):
    query = appointment.select().where(appointment.c.appointment_id == id)
    result = await database.fetch_one(query=query)
    if result:
        return {
            field: result[field]
            for field in AppointmentOut.__fields__.keys()
            if field in result
        }
    return result


async def delete_appointment(id: int):
    query = appointment.delete().where(appointment.c.appointment_id == id)
    return await database.execute(query=query)


async def update_appointment(id: int, payload: AppointmentUpdate):
    query = appointment.update().where(appointment.c.appointment_id == id).values(**payload.dict())
    await database.execute(query=query)
    return await get_appointment(id)
from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import AppointmentOut, AppointmentCreate, AppointmentUpdate
from app.api import db_manager

import pandas as pd

appointment = APIRouter()


@appointment.post('/', response_model=AppointmentOut, status_code=201)
async def create_appointment(payload: AppointmentCreate):
    appointment_id = await db_manager.add_appointment(payload)
    response = {'appointment_id': appointment_id, **payload.dict()}
    return response


@appointment.get('/', response_model=List[AppointmentOut])
async def get_appointments():
    return await db_manager.get_all_appointments()


@appointment.get('/{id}/', response_model=AppointmentOut)
async def get_appointment(id: int):
    appointment = await db_manager.get_appointment(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@appointment.put('/{id}/', response_model=AppointmentOut)
async def update_appointment(id: int, payload: AppointmentUpdate):
    appointment = await db_manager.get_appointment(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return await db_manager.update_appointment(id, payload)


@appointment.delete('/{id}/', response_model=None)
async def delete_appointment(id: int):
    appointment = await db_manager.get_appointment(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return await db_manager.delete_appointment(id)


@appointment.get('/patients_per_hospital')
async def patients_per_hospital():
    appointments = await db_manager.get_all_appointments()
    appointments_df = pd.DataFrame(appointments)

    doctors = await db_manager.get_all_doctors()
    doctors_df = pd.DataFrame(doctors)

    hospitals = await db_manager.get_all_hospitals()
    hospitals_df = pd.DataFrame(hospitals)

    merged_df = pd.merge(appointments_df, doctors_df, on='doctor_id', how='left')

    merged_df = pd.merge(merged_df, hospitals_df, on='hospital_id', how='left')

    patients = await db_manager.get_all_patients()
    patients_df = pd.DataFrame(patients)
    result_df = pd.merge(merged_df, patients_df, on='patient_id', how='left')

    patients_per_hospital = result_df.groupby(['hospital_name', 'hospital_address']).size().reset_index(name='Number of Patients')

    result = patients_per_hospital.to_dict(orient='records')
    return result

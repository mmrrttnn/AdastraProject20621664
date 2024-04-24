from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import PatientOut, PatientCreate, PatientUpdate
from app.api import db_manager

import pandas as pd
from typing import List, Dict, Any

patient = APIRouter()


@patient.post('/', response_model=PatientOut, status_code=201)
async def create_patient(payload: PatientCreate):
    patient_id = await db_manager.add_patient(payload)
    response = {'patient_id': patient_id, **payload.dict()}
    return response


@patient.get('/', response_model=List[PatientOut])
async def get_patients():
    return await db_manager.get_all_patients()


@patient.get('/{id}/', response_model=PatientOut)
async def get_patient(id: int):
    patient = await db_manager.get_patient(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@patient.put('/{id}/', response_model=PatientOut)
async def update_patient(id: int, payload: PatientUpdate):
    patient = await db_manager.get_patient(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return await db_manager.update_patient(id, payload)


@patient.delete('/{id}/', response_model=None)
async def delete_patient(id: int):
    patient = await db_manager.get_patient(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return await db_manager.delete_patient(id)


@patient.get('/patients_details', response_model=List[Dict[str, Any]])
async def get_patients_details():
    patients = await db_manager.get_all_patients()
    appointments = await db_manager.get_all_appointments()
    hospitals = await db_manager.get_all_hospitals()
    doctors = await db_manager.get_all_doctors()

    patients_df = pd.DataFrame(patients)
    appointments_df = pd.DataFrame(appointments)
    hospitals_df = pd.DataFrame(hospitals)
    doctors_df = pd.DataFrame(doctors)

    appt_patients_df = pd.merge(appointments_df, patients_df, on='patient_id', how='left')

    appt_doctors_df = pd.merge(appt_patients_df, doctors_df, on='doctor_id', how='left')

    appt_hospitals_df = pd.merge(appt_doctors_df, hospitals_df, on='hospital_id', how='left')

    columns = ['patient_id', 'patient_name', 'appointment_id', 'appointment_date',
               'doctor_id', 'doctor_name', 'hospital_id', 'hospital_name', 'hospital_address']
    result_df = appt_hospitals_df[columns].fillna('Not Available')

    result = result_df.to_dict(orient='records')
    return result


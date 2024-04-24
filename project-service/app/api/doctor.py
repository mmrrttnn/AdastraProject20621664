from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import DoctorOut, DoctorCreate, DoctorUpdate
from app.api import db_manager

import pandas as pd

doctor = APIRouter()


@doctor.post('/', response_model=DoctorOut, status_code=201)
async def create_doctor(payload: DoctorCreate):
    doctor_id = await db_manager.add_doctor(payload)
    response = {'doctor_id': doctor_id, **payload.dict()}
    return response


@doctor.get('/', response_model=List[DoctorOut])
async def get_doctors():
    return await db_manager.get_all_doctors()


@doctor.get('/{id}/', response_model=DoctorOut)
async def get_doctor(id: int):
    doctor = await db_manager.get_doctor(id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@doctor.put('/{id}/', response_model=DoctorOut)
async def update_doctor(id: int, payload: DoctorUpdate):
    doctor = await db_manager.get_doctor(id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return await db_manager.update_doctor(id, payload)


@doctor.delete('/{id}/', response_model=None)
async def delete_doctor(id: int):
    doctor = await db_manager.get_doctor(id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return await db_manager.delete_doctor(id)


@doctor.get('/doctors_with_hospitals')
async def doctors_with_hospitals():
    doctors = await db_manager.get_all_doctors()
    hospitals = await db_manager.get_all_hospitals()

    doctors_df = pd.DataFrame(doctors)
    hospitals_df = pd.DataFrame(hospitals)

    doctors_hospitals_df = pd.merge(doctors_df, hospitals_df, on='hospital_id', how='left')
    return doctors_hospitals_df.to_dict(orient='records')


@doctor.get('/doctors_by_specialization/{specialization}')
async def doctors_by_specialization(specialization: str):
    doctors = await db_manager.get_all_doctors()
    doctors_df = pd.DataFrame(doctors)

    filtered_doctors_df = doctors_df[doctors_df['doctor_specialisation'] == specialization]
    return filtered_doctors_df.to_dict(orient='records')


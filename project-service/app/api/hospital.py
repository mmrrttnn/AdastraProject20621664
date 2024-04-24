from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import HospitalOut, HospitalCreate, HospitalUpdate
from app.api import db_manager

import pandas as pd

hospital = APIRouter()


@hospital.post('/', response_model=HospitalOut, status_code=201)
async def create_hospital(payload: HospitalCreate):
    hospital_id = await db_manager.add_hospital(payload)
    response = {'hospital_id': hospital_id, **payload.dict()}
    return response


@hospital.get('/', response_model=List[HospitalOut])
async def get_hospitals():
    return await db_manager.get_all_hospitals()


@hospital.get('/{id}/', response_model=HospitalOut)
async def get_hospital(id: int):
    hospital = await db_manager.get_hospital(id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@hospital.put('/{id}/', response_model=HospitalOut)
async def update_hospital(id: int, payload: HospitalUpdate):
    hospital = await db_manager.get_hospital(id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    return await db_manager.update_hospital(id, payload)


@hospital.delete('/{id}/', response_model=None)
async def delete_hospital(id: int):
    hospital = await db_manager.get_hospital(id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return await db_manager.delete_hospital(id)


@hospital.get('/hospitals_specializations')
async def hospitals_specializations():
    hospitals = await db_manager.get_all_hospitals()
    doctors = await db_manager.get_all_doctors()

    hospitals_df = pd.DataFrame(hospitals)
    doctors_df = pd.DataFrame(doctors)

    merged_df = pd.merge(hospitals_df, doctors_df, on='hospital_id', how='left')

    hospital_specializations = merged_df.groupby(['hospital_name', 'hospital_address'])['doctor_specialisation'].apply(list).reset_index()

    result = hospital_specializations.to_dict(orient='records')
    return result

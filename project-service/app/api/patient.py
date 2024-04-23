from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import PatientOut, PatientCreate, PatientUpdate
from app.api import db_manager

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
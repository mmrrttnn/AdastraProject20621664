from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import HospitalOut, HospitalCreate, HospitalUpdate
from app.api import db_manager

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
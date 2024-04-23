from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import DoctorOut, DoctorCreate, DoctorUpdate
from app.api import db_manager

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
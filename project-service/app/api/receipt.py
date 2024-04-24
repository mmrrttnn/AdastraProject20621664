from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import ReceiptOut, ReceiptCreate, ReceiptUpdate
from app.api import db_manager

receipt = APIRouter()


@receipt.post('/', response_model=ReceiptOut, status_code=201)
async def create_receipt(payload: ReceiptCreate):
    receipt_id = await db_manager.add_receipt(payload)
    response = {'receipt_id': receipt_id, **payload.dict()}
    return response


@receipt.get('/', response_model=List[ReceiptOut])
async def get_receipts():
    return await db_manager.get_all_receipts()


@receipt.get('/{id}/', response_model=ReceiptOut)
async def get_receipt(id: int):
    receipt = await db_manager.get_receipt(id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@receipt.put('/{id}/', response_model=ReceiptOut)
async def update_receipt(id: int, payload: ReceiptUpdate):
    receipt = await db_manager.get_receipt(id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return await db_manager.update_receipt(id, payload)


@receipt.delete('/{id}/', response_model=None)
async def delete_receipt(id: int):
    receipt = await db_manager.get_receipt(id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return await db_manager.delete_receipt(id)
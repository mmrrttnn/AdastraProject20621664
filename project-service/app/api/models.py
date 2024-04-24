from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date


class HospitalBase(BaseModel):
    hospital_name: str
    hospital_address: str


class HospitalCreate(HospitalBase):
    pass

class HospitalOut(HospitalBase):
    hospital_id: int

    class Config:
        orm_module = True


class HospitalUpdate(BaseModel):
    hospital_name: Optional[str] = None
    hospital_address: Optional[str] = None


class DoctorBase(BaseModel):
    doctor_name: str
    doctor_specialisation: str
    doctor_phone_number: str
    hospital_id: int


class DoctorCreate(DoctorBase):
    pass


class DoctorOut(DoctorBase):
    doctor_id: int

    class Config:
        orm_module = True


class DoctorUpdate(DoctorBase):
    doctor_name: Optional[str] = None
    doctor_specialisation: Optional[str] = None
    doctor_phone_number: Optional[str] = None
    hospital_id: Optional[int] = None


class PatientBase(BaseModel):
    patient_name: str
    patient_number: str


class PatientCreate(PatientBase):
    pass


class PatientOut(PatientBase):
    patient_id: int

    class Config:
        orm_module = True


class PatientUpdate(PatientBase):
    patient_name: Optional[str] = None
    patient_number: Optional[str] = None


class ReceiptBase(BaseModel):
    receipt_text: str


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptOut(ReceiptBase):
    receipt_id: int

    class Config:
        orm_module = True


class ReceiptUpdate(ReceiptBase):
    receipt_id: Optional[int] = None
    receipt_text: Optional[str] = None


class AppointmentBase(BaseModel):
    appointment_date: date
    appointment_reason: str
    doctor_id: int
    patient_id: int
    receipt_id: int


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    appointment_id: int

    class Config:
        orm_module = True


class AppointmentUpdate(AppointmentBase):
    appointment_date: Optional[date] = None
    appointment_reason: Optional[str] = None
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None
    receipt_id: Optional[int] = None


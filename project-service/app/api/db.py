import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, DateTime
from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

hospital = Table(
    'hospital', metadata,
    Column('hospital_id', Integer, primary_key=True),
    Column('hospital_name', String(255)),
    Column('hospital_address', String(255))
)

doctor = Table(
    'doctor', metadata,
    Column('doctor_id', Integer, primary_key=True),
    Column('doctor_name', String(255)),
    Column('doctor_specialisation', String(255)),
    Column('doctor_phone_number', String(255)),
    Column('hospital_id', Integer, ForeignKey('hospital.hospital_id'))
)

patient = Table(
    'patient', metadata,
    Column('patient_id', Integer, primary_key=True),
    Column('patient_name', String(255)),
    Column('patient_number', String(255))
)

receipt = Table(
    'receipt', metadata,
    Column('receipt_id', Integer, primary_key=True),
    Column('receipt_text', String(255))
)

appointment = Table(
    'appointment', metadata,
    Column('appointment_id', Integer, primary_key=True),
    Column('appointment_date', DateTime),
    Column('appointment_reason', String(255)),
    Column('doctor_id', Integer, ForeignKey('doctor.doctor_id')),
    Column('patient_id', Integer, ForeignKey('patient.patient_id')),
    Column('receipt_id', Integer, ForeignKey('receipt.receipt_id'))
)

database = Database(DATABASE_URI)

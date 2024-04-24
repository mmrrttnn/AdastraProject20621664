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


def reset_tables():
    with engine.connect() as connection:
        connection.execute(appointment.delete())
        connection.execute(doctor.delete())
        connection.execute(patient.delete())
        connection.execute(receipt.delete())
        connection.execute(hospital.delete())

        connection.execute("ALTER SEQUENCE hospital_hospital_id_seq RESTART WITH 1")
        connection.execute("ALTER SEQUENCE doctor_doctor_id_seq RESTART WITH 1")
        connection.execute("ALTER SEQUENCE patient_patient_id_seq RESTART WITH 1")
        connection.execute("ALTER SEQUENCE receipt_receipt_id_seq RESTART WITH 1")
        connection.execute("ALTER SEQUENCE appointment_appointment_id_seq RESTART WITH 1")


reset_tables()

with engine.connect() as connection:
    connection.execute(
        hospital.insert(),
            [
                {'hospital_name': 'City Hospital', 'hospital_address': 'Varna'},
                {'hospital_name': 'Cardiac Hospital', 'hospital_address': 'Burgas'},
                {'hospital_name': 'Kids Clinic', 'hospital_address': 'Varna'},
                {'hospital_name': 'Town Clinic', 'hospital_address': 'Veliko Tarnovo'}
            ]
    )

    connection.execute(
        doctor.insert(),
            [
                {'doctor_name': 'Dr. Pavlov', 'doctor_specialisation': 'Cardiology', 'doctor_phone_number': '+39393', 'hospital_id': 1},
                {'doctor_name': 'Dr. Drumev', 'doctor_specialisation': 'Surgery', 'doctor_phone_number': '+39393', 'hospital_id': 1},
                {'doctor_name': 'Dr. Ivanova', 'doctor_specialisation': 'Pediatry', 'doctor_phone_number': '+39393', 'hospital_id': 1},
                {'doctor_name': 'Dr. Petrov', 'doctor_specialisation': 'Surgery', 'doctor_phone_number': '+39393', 'hospital_id': 2},
                {'doctor_name': 'Dr. Mihnev', 'doctor_specialisation': 'Cardiology', 'doctor_phone_number': '+39393', 'hospital_id': 2},
                {'doctor_name': 'Dr. Stefanov', 'doctor_specialisation': 'Traumatology', 'doctor_phone_number': '+39393', 'hospital_id': 3},
                {'doctor_name': 'Dr. Yovchev', 'doctor_specialisation': 'Traumatology', 'doctor_phone_number': '+39393', 'hospital_id': 4},
                {'doctor_name': 'Dr. Dimov', 'doctor_specialisation': 'Emergency Response', 'doctor_phone_number': '+39393', 'hospital_id': 4},
                {'doctor_name': 'Dr. Karaivanova', 'doctor_specialisation': 'Infections', 'doctor_phone_number': '+39393', 'hospital_id': 3},
                {'doctor_name': 'Dr. Cholakov', 'doctor_specialisation': 'Pediatry', 'doctor_phone_number': '+39393', 'hospital_id': 3},
                {'doctor_name': 'Dr. Sins', 'doctor_specialisation': 'Orthopedy', 'doctor_phone_number': '+39393', 'hospital_id': 4},
                {'doctor_name': 'Dr. Lee', 'doctor_specialisation': 'Orthopedy', 'doctor_phone_number': '+39393', 'hospital_id': 1},
            ]
    )

    connection.execute(
        patient.insert(),
            [
                {'patient_name': 'Stoyan', 'patient_number': '+32324'},
                {'patient_name': 'Maria', 'patient_number': '+32324'},
                {'patient_name': 'Yoanna', 'patient_number': '+32324'},
                {'patient_name': 'Ivan', 'patient_number': '+32324'},
                {'patient_name': 'Mihail', 'patient_number': '+32324'},
                {'patient_name': 'Stefan', 'patient_number': '+32324'},
                {'patient_name': 'Karina', 'patient_number': '+32324'},
                {'patient_name': 'Galena', 'patient_number': '+32324'}
            ]
    )

    connection.execute(
        receipt.insert(),
            [
                {'receipt_text': 'R1'},
                {'receipt_text': 'R2'},
                {'receipt_text': 'R3'},
                {'receipt_text': 'R4'},
                {'receipt_text': 'R5'},
                {'receipt_text': 'R6'},
                {'receipt_text': 'R7'},
                {'receipt_text': 'R8'}
            ]
    )

    connection.execute(
        appointment.insert(),
            [
                {'appointment_date': '2024-10-10', 'appointment_reason': 'Check-up', 'doctor_id': 3, 'patient_id': 1, 'receipt_id': 3},
                {'appointment_date': '2024-10-10', 'appointment_reason': 'Heart Cancer', 'doctor_id': 1, 'patient_id': 2, 'receipt_id': 2},
                {'appointment_date': '2024-10-10', 'appointment_reason': 'Pre-surgery check-up', 'doctor_id': 2, 'patient_id': 3, 'receipt_id': 1},
                {'appointment_date': '2024-10-11', 'appointment_reason': 'Broken Leg', 'doctor_id': 7 , 'patient_id': 4 , 'receipt_id': 4},
                {'appointment_date': '2024-10-11', 'appointment_reason': 'Allergy', 'doctor_id': 4 , 'patient_id': 5, 'receipt_id': 7},
                {'appointment_date': '2024-10-11', 'appointment_reason': 'Post-op Check', 'doctor_id': 5, 'patient_id': 6, 'receipt_id': 5},
                {'appointment_date': '2024-10-12', 'appointment_reason': 'Broken Arm', 'doctor_id': 12, 'patient_id': 7, 'receipt_id': 6}
            ]

    )


database = Database(DATABASE_URI)

from app.api.db import metadata, database, engine
from app.api.appointment import appointment
from app.api.doctor import doctor
from app.api.hospital import hospital
from app.api.patient import patient
from app.api.receipt import receipt

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/project/openapi.json",
              docs_url="/api/v1/project/docs")

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "message": "An error occurred with the database operation", "detail": str(exc)}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred.",
                 "detail": str(exc)},
    )


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(hospital, prefix='/api/v1/hospital',
                   tags=['hospital'])
app.include_router(doctor, prefix='/api/v1/doctor',
                   tags=['doctor'])
app.include_router(patient, prefix='/api/v1/patient',
                   tags=['patient'])
app.include_router(appointment, prefix='/api/v1/appointment',
                   tags=['appointment'])
app.include_router(receipt, prefix='/api/v1/receipt',
                   tags=['receipt'])
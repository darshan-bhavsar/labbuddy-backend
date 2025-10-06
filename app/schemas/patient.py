from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from ..models.patient import Gender


class PatientBase(BaseModel):
    name: str
    dob: date
    gender: Gender
    phone: Optional[str] = None
    address: Optional[str] = None
    has_mediclaim: bool = False


class PatientCreate(PatientBase):
    lab_id: int
    hospital_id: Optional[int] = None


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    has_mediclaim: Optional[bool] = None
    hospital_id: Optional[int] = None


class PatientResponse(PatientBase):
    patient_id: int
    lab_id: int
    hospital_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

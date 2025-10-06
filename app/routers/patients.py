from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, date

from ..routers.auth_simple import get_current_user, User

router = APIRouter(prefix="/patients", tags=["patients"])

class PatientResponse(BaseModel):
    patient_id: int
    name: str
    dob: date
    gender: str
    phone: str
    address: str
    has_mediclaim: bool
    created_at: datetime

# Sample patients data
SAMPLE_PATIENTS = [
    {
        "patient_id": 1,
        "name": "John Smith",
        "dob": date(1985, 5, 15),
        "gender": "MALE",
        "phone": "+1-555-1001",
        "address": "123 Oak Street, City Center",
        "has_mediclaim": True,
        "created_at": datetime.now()
    },
    {
        "patient_id": 2,
        "name": "Sarah Johnson",
        "dob": date(1990, 8, 22),
        "gender": "FEMALE",
        "phone": "+1-555-1002",
        "address": "456 Pine Avenue, Metro District",
        "has_mediclaim": False,
        "created_at": datetime.now()
    },
    {
        "patient_id": 3,
        "name": "Michael Brown",
        "dob": date(1978, 12, 3),
        "gender": "MALE",
        "phone": "+1-555-1003",
        "address": "789 Elm Road, Regional Area",
        "has_mediclaim": True,
        "created_at": datetime.now()
    },
    {
        "patient_id": 4,
        "name": "Emily Davis",
        "dob": date(1995, 3, 18),
        "gender": "FEMALE",
        "phone": "+1-555-1004",
        "address": "321 Maple Lane, Downtown",
        "has_mediclaim": True,
        "created_at": datetime.now()
    }
]

@router.get("/", response_model=List[PatientResponse])
def get_patients(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Get all patients."""
    return SAMPLE_PATIENTS[skip:skip+limit]

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get a specific patient by ID."""
    patient = next((p for p in SAMPLE_PATIENTS if p["patient_id"] == patient_id), None)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    return patient

@router.post("/", response_model=PatientResponse)
def create_patient(
    patient_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Create a new patient."""
    new_patient = {
        "patient_id": len(SAMPLE_PATIENTS) + 1,
        "name": patient_data.get("name", "New Patient"),
        "dob": date.today(),
        "gender": patient_data.get("gender", "MALE"),
        "phone": patient_data.get("phone", "+1-555-0000"),
        "address": patient_data.get("address", "123 New Address"),
        "has_mediclaim": patient_data.get("has_mediclaim", False),
        "created_at": datetime.now()
    }
    SAMPLE_PATIENTS.append(new_patient)
    return new_patient

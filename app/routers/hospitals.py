from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from ..routers.auth_simple import get_db, get_current_user, User

router = APIRouter(prefix="/hospitals", tags=["hospitals"])

class HospitalResponse(BaseModel):
    hospital_id: int
    name: str
    address: str
    contact_info: str
    status: str
    created_at: datetime

# Sample hospitals data
SAMPLE_HOSPITALS = [
    {
        "hospital_id": 1,
        "name": "City General Hospital",
        "address": "123 Main Street, City Center",
        "contact_info": "contact@citygeneral.com, +1-555-0101",
        "status": "ACTIVE",
        "created_at": datetime.now()
    },
    {
        "hospital_id": 2,
        "name": "Metro Health Center",
        "address": "456 Health Avenue, Metro District",
        "contact_info": "info@metrohealth.com, +1-555-0102",
        "status": "ACTIVE",
        "created_at": datetime.now()
    },
    {
        "hospital_id": 3,
        "name": "Regional Medical Center",
        "address": "789 Medical Blvd, Regional Area",
        "contact_info": "admin@regionalmed.com, +1-555-0103",
        "status": "ACTIVE",
        "created_at": datetime.now()
    }
]

@router.get("/", response_model=List[HospitalResponse])
def get_hospitals(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Get all hospitals."""
    return SAMPLE_HOSPITALS[skip:skip+limit]

@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital(
    hospital_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get a specific hospital by ID."""
    hospital = next((h for h in SAMPLE_HOSPITALS if h["hospital_id"] == hospital_id), None)
    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )
    return hospital

@router.post("/", response_model=HospitalResponse)
def create_hospital(
    hospital_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Create a new hospital."""
    new_hospital = {
        "hospital_id": len(SAMPLE_HOSPITALS) + 1,
        "name": hospital_data.get("name", "New Hospital"),
        "address": hospital_data.get("address", "123 New Street"),
        "contact_info": hospital_data.get("contact_info", "contact@newhospital.com"),
        "status": "ACTIVE",
        "created_at": datetime.now()
    }
    SAMPLE_HOSPITALS.append(new_hospital)
    return new_hospital

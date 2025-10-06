from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

from ..routers.auth_simple import get_current_user, User

router = APIRouter(prefix="/tests", tags=["tests"])

class TestMasterResponse(BaseModel):
    test_id: int
    name: str
    description: str
    sample_type: str
    turnaround_time: int

class LabTestResponse(BaseModel):
    lab_test_id: int
    test_id: int
    test_name: str
    price: float
    status: str

# Sample test masters data
SAMPLE_TEST_MASTERS = [
    {
        "test_id": 1,
        "name": "Complete Blood Count (CBC)",
        "description": "A blood test that measures different components of blood",
        "sample_type": "Blood",
        "turnaround_time": 24
    },
    {
        "test_id": 2,
        "name": "Blood Glucose",
        "description": "Measures blood sugar levels",
        "sample_type": "Blood",
        "turnaround_time": 4
    },
    {
        "test_id": 3,
        "name": "Urine Analysis",
        "description": "Complete analysis of urine sample",
        "sample_type": "Urine",
        "turnaround_time": 6
    },
    {
        "test_id": 4,
        "name": "Lipid Profile",
        "description": "Cholesterol and triglyceride levels",
        "sample_type": "Blood",
        "turnaround_time": 24
    },
    {
        "test_id": 5,
        "name": "Thyroid Function Test",
        "description": "TSH, T3, T4 levels",
        "sample_type": "Blood",
        "turnaround_time": 48
    }
]

# Sample lab tests data
SAMPLE_LAB_TESTS = [
    {
        "lab_test_id": 1,
        "test_id": 1,
        "test_name": "Complete Blood Count (CBC)",
        "price": 25.00,
        "status": "ACTIVE"
    },
    {
        "lab_test_id": 2,
        "test_id": 2,
        "test_name": "Blood Glucose",
        "price": 15.00,
        "status": "ACTIVE"
    },
    {
        "lab_test_id": 3,
        "test_id": 3,
        "test_name": "Urine Analysis",
        "price": 20.00,
        "status": "ACTIVE"
    },
    {
        "lab_test_id": 4,
        "test_id": 4,
        "test_name": "Lipid Profile",
        "price": 35.00,
        "status": "ACTIVE"
    },
    {
        "lab_test_id": 5,
        "test_id": 5,
        "test_name": "Thyroid Function Test",
        "price": 45.00,
        "status": "ACTIVE"
    }
]

@router.get("/master", response_model=List[TestMasterResponse])
def get_test_masters(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Get all available test masters."""
    return SAMPLE_TEST_MASTERS[skip:skip+limit]

@router.get("/master/{test_id}", response_model=TestMasterResponse)
def get_test_master(
    test_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get a specific test master by ID."""
    test = next((t for t in SAMPLE_TEST_MASTERS if t["test_id"] == test_id), None)
    if not test:
        raise HTTPException(
            status_code=404,
            detail="Test master not found"
        )
    return test

@router.get("/lab/1", response_model=List[LabTestResponse])
def get_lab_tests(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Get all tests available for the lab."""
    return SAMPLE_LAB_TESTS[skip:skip+limit]

@router.post("/lab", response_model=LabTestResponse)
def add_to_lab(
    lab_test_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Add a test to lab's available tests."""
    new_lab_test = {
        "lab_test_id": len(SAMPLE_LAB_TESTS) + 1,
        "test_id": lab_test_data.get("test_id", 1),
        "test_name": "New Test",
        "price": lab_test_data.get("price", 25.00),
        "status": "ACTIVE"
    }
    SAMPLE_LAB_TESTS.append(new_lab_test)
    return new_lab_test

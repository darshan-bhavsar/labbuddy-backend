from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

from ..routers.auth_simple import get_current_user, User

router = APIRouter(prefix="/reports", tags=["reports"])

class ReportResponse(BaseModel):
    report_id: int
    patient_id: int
    patient_name: str
    hospital_id: int
    hospital_name: str
    status: str
    created_at: datetime
    updated_at: datetime

# Sample reports data
SAMPLE_REPORTS = [
    {
        "report_id": 1,
        "patient_id": 1,
        "patient_name": "John Smith",
        "hospital_id": 1,
        "hospital_name": "City General Hospital",
        "status": "REPORT_READY",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "report_id": 2,
        "patient_id": 2,
        "patient_name": "Sarah Johnson",
        "hospital_id": 2,
        "hospital_name": "Metro Health Center",
        "status": "IN_PROCESS",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "report_id": 3,
        "patient_id": 3,
        "patient_name": "Michael Brown",
        "hospital_id": 1,
        "hospital_name": "City General Hospital",
        "status": "SAMPLE_COLLECTED",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "report_id": 4,
        "patient_id": 4,
        "patient_name": "Emily Davis",
        "hospital_id": 3,
        "hospital_name": "Regional Medical Center",
        "status": "DELIVERED",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "report_id": 5,
        "patient_id": 1,
        "patient_name": "John Smith",
        "hospital_id": 2,
        "hospital_name": "Metro Health Center",
        "status": "BOOKED",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

@router.get("/", response_model=List[ReportResponse])
def get_reports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Get all reports."""
    return SAMPLE_REPORTS[skip:skip+limit]

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get a specific report by ID."""
    report = next((r for r in SAMPLE_REPORTS if r["report_id"] == report_id), None)
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    return report

@router.post("/", response_model=ReportResponse)
def create_report(
    report_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Create a new report."""
    new_report = {
        "report_id": len(SAMPLE_REPORTS) + 1,
        "patient_id": report_data.get("patient_id", 1),
        "patient_name": "New Patient",
        "hospital_id": report_data.get("hospital_id", 1),
        "hospital_name": "New Hospital",
        "status": "BOOKED",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    SAMPLE_REPORTS.append(new_report)
    return new_report

@router.put("/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    report_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Update report status."""
    report = next((r for r in SAMPLE_REPORTS if r["report_id"] == report_id), None)
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    
    if "status" in report_data:
        report["status"] = report_data["status"]
        report["updated_at"] = datetime.now()
    
    return report

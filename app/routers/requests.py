
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportResponse, ReportUpdate
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/requests", tags=["lab requests"])

# Helper to check user role
def require_role(user: User, allowed_roles: list[str]):
    if user.role.name not in allowed_roles:
        raise HTTPException(status_code=403, detail="Forbidden")

# List all sample collection requests
def get_lab_requests(db: Session):
    return db.query(Report).all()

@router.get("/", response_model=list[ReportResponse])
def list_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_lab_requests(db)

# Hospital can create/upload a report
@router.post("/", response_model=ReportResponse)
def create_report(report: ReportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_role(current_user, ["HOSPITAL_USER"])
    new_report = Report(
        lab_id=report.lab_id,
        hospital_id=report.hospital_id,
        patient_id=report.patient_id,
        status="BOOKED"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

# Lab can update report status
@router.patch("/{report_id}/status", response_model=ReportResponse)
def update_report_status(report_id: int, update: ReportUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_role(current_user, ["LAB_ADMIN", "LAB_STAFF"])
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if update.status:
        report.status = update.status
        db.commit()
        db.refresh(report)
    return report

# Confirm pickup for a request
@router.post("/{request_id}/confirm-pickup")
def confirm_pickup(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.report_id == request_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Request not found")
    report.status = "IN_PROCESS"
    db.commit()
    return {"message": "Pickup confirmed", "request_id": request_id}

# Upload report for a request
@router.post("/{request_id}/upload-report")
def upload_report(request_id: int, report_data: ReportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.report_id == request_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Request not found")
    # You may want to update report result or attach files here
    report.status = "REPORT_READY"
    db.commit()
    return {"message": "Report uploaded", "request_id": request_id}

# View details for a request
@router.get("/{request_id}", response_model=ReportResponse)
def view_request_details(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.report_id == request_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Request not found")
    return report

# Confirm pickup for a request
@router.post("/{request_id}/confirm-pickup")
def confirm_pickup(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == request_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Request not found")
    report.status = "In Progress"
    db.commit()
    return {"message": "Pickup confirmed", "request_id": request_id}

# Upload report for a request
@router.post("/{request_id}/upload-report")
def upload_report(request_id: int, report_data: ReportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == request_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Request not found")
    report.result = report_data.result
    report.status = "Completed"
    db.commit()
    return {"message": "Report uploaded", "request_id": request_id}

# View details for a request
@router.get("/{request_id}", response_model=ReportResponse)
def view_request_details(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    report = db.query(Report).filter(Report.id == request_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Request not found")
    return report

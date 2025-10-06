from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.report import Report, ReportTest, ReportFile
from ..models.user import User
from ..schemas.report import ReportCreate, ReportResponse, ReportUpdate, ReportFileResponse
from ..utils.security import require_lab_staff, require_hospital_user
from ..services.file_upload import FileUploadService
from ..services.notification import NotificationService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/", response_model=ReportResponse)
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Create a new report booking."""
    # Verify lab exists
    from ..models.lab import Lab
    lab = db.query(Lab).filter(Lab.lab_id == report.lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=404,
            detail="Lab not found"
        )
    
    # Verify patient exists
    from ..models.patient import Patient
    patient = db.query(Patient).filter(Patient.patient_id == report.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    
    # Verify hospital exists if provided
    if report.hospital_id:
        from ..models.hospital import Hospital
        hospital = db.query(Hospital).filter(Hospital.hospital_id == report.hospital_id).first()
        if not hospital:
            raise HTTPException(
                status_code=404,
                detail="Hospital not found"
            )
    
    # Verify lab tests exist and belong to the lab
    from ..models.test import LabTest
    lab_tests = db.query(LabTest).filter(
        LabTest.lab_test_id.in_(report.lab_test_ids),
        LabTest.lab_id == report.lab_id
    ).all()
    
    if len(lab_tests) != len(report.lab_test_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more lab tests not found or don't belong to the lab"
        )
    
    # Create report
    db_report = Report(
        lab_id=report.lab_id,
        hospital_id=report.hospital_id,
        patient_id=report.patient_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    # Create report tests
    for lab_test in lab_tests:
        report_test = ReportTest(
            report_id=db_report.report_id,
            lab_test_id=lab_test.lab_test_id
        )
        db.add(report_test)
    
    db.commit()
    
    # Send notifications
    notification_service = NotificationService(db)
    notification_service.send_report_created_notifications(db_report)
    
    return db_report


@router.post("/request", response_model=ReportResponse)
def request_report(
    report: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hospital_user)
):
    """Hospital requests a new report booking. Same validations as lab create."""
    # Verify lab exists
    from ..models.lab import Lab
    lab = db.query(Lab).filter(Lab.lab_id == report.lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    # Verify patient exists
    from ..models.patient import Patient
    patient = db.query(Patient).filter(Patient.patient_id == report.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    # hospital_id must be provided by hospital user
    if not report.hospital_id:
        raise HTTPException(status_code=400, detail="hospital_id is required")
    from ..models.hospital import Hospital
    hospital = db.query(Hospital).filter(Hospital.hospital_id == report.hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    # Verify lab tests
    from ..models.test import LabTest
    lab_tests = db.query(LabTest).filter(
        LabTest.lab_test_id.in_(report.lab_test_ids),
        LabTest.lab_id == report.lab_id
    ).all()
    if len(lab_tests) != len(report.lab_test_ids):
        raise HTTPException(status_code=400, detail="One or more lab tests not found or don't belong to the lab")
    # Create report with BOOKED status
    db_report = Report(
        lab_id=report.lab_id,
        hospital_id=report.hospital_id,
        patient_id=report.patient_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    # Create report tests
    for lab_test in lab_tests:
        db.add(ReportTest(report_id=db_report.report_id, lab_test_id=lab_test.lab_test_id))
    db.commit()
    # Notify lab
    notification_service = NotificationService(db)
    notification_service.send_report_created_notifications(db_report)
    return db_report


@router.get("/", response_model=List[ReportResponse])
def get_reports(
    lab_id: int = None,
    hospital_id: int = None,
    patient_id: int = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Get reports with optional filters."""
    query = db.query(Report)
    
    if lab_id:
        query = query.filter(Report.lab_id == lab_id)
    if hospital_id:
        query = query.filter(Report.hospital_id == hospital_id)
    if patient_id:
        query = query.filter(Report.patient_id == patient_id)
    if status:
        from ..models.report import ReportStatus
        query = query.filter(Report.status == ReportStatus(status))
    
    reports = query.offset(skip).limit(limit).all()
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Get a specific report by ID."""
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    return report


@router.put("/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    report_update: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Update report status."""
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    
    old_status = report.status
    update_data = report_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(report, field, value)
    
    db.commit()
    db.refresh(report)
    
    # Send notifications if status changed
    if old_status != report.status:
        notification_service = NotificationService(db)
        notification_service.send_status_change_notifications(report, old_status)
    
    return report


@router.post("/{report_id}/upload", response_model=ReportFileResponse)
def upload_report_file(
    report_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Upload a report file to S3 and save metadata."""
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    # Validate and upload to S3
    uploader = FileUploadService()
    uploader.validate_file(file, max_size_mb=20, allowed_types=["application/pdf"])
    file_url = uploader.upload_file_to_s3(file, folder=f"reports/{report_id}")
    
    report_file = ReportFile(
        report_id=report_id,
        file_url=file_url,
        uploaded_by=current_user.user_id
    )
    
    db.add(report_file)
    db.commit()
    db.refresh(report_file)
    
    return report_file


@router.get("/{report_id}/files", response_model=List[ReportFileResponse])
def get_report_files(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Get all files for a report."""
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )
    
    files = db.query(ReportFile).filter(ReportFile.report_id == report_id).all()
    return files


@router.get("/{report_id}/files/{report_file_id}/download")
def download_report_file(
    report_id: int,
    report_file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hospital_user)
):
    """Return a presigned URL for the hospital to download the report PDF."""
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report_file = db.query(ReportFile).filter(
        ReportFile.report_file_id == report_file_id,
        ReportFile.report_id == report_id
    ).first()
    if not report_file:
        raise HTTPException(status_code=404, detail="Report file not found")
    uploader = FileUploadService()
    presigned = uploader.get_presigned_url(report_file.file_url, expiration=3600)
    return {"url": presigned or report_file.file_url}

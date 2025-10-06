from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.report import ReportStatus


class ReportBase(BaseModel):
    patient_id: int
    hospital_id: Optional[int] = None


class ReportCreate(ReportBase):
    lab_id: int
    lab_test_ids: List[int]  # Tests to be performed


class ReportUpdate(BaseModel):
    status: Optional[ReportStatus] = None


class ReportResponse(ReportBase):
    report_id: int
    lab_id: int
    status: ReportStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    patient: Optional[dict] = None  # Patient details
    hospital: Optional[dict] = None  # Hospital details
    report_tests: Optional[List[dict]] = None
    report_files: Optional[List[dict]] = None

    class Config:
        from_attributes = True


class ReportFileResponse(BaseModel):
    report_file_id: int
    report_id: int
    file_url: str
    uploaded_by: int
    uploaded_at: datetime
    is_signed: bool

    class Config:
        from_attributes = True


class ReportTestResponse(BaseModel):
    report_test_id: int
    report_id: int
    lab_test_id: int
    result_value: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

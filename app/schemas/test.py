from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.test import LabTestStatus


class TestMasterResponse(BaseModel):
    test_id: int
    name: str
    description: Optional[str] = None
    sample_type: str
    turnaround_time: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LabTestBase(BaseModel):
    test_id: int
    price: Optional[float] = None
    status: LabTestStatus = LabTestStatus.ACTIVE


class LabTestCreate(LabTestBase):
    lab_id: int


class LabTestResponse(LabTestBase):
    lab_test_id: int
    lab_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    test_master: Optional[TestMasterResponse] = None

    class Config:
        from_attributes = True

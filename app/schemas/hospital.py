from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.hospital import HospitalStatus


class HospitalBase(BaseModel):
    name: str
    address: str
    contact_info: str


class HospitalCreate(HospitalBase):
    lab_id: int
    status: Optional[HospitalStatus] = HospitalStatus.ACTIVE


class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_info: Optional[str] = None
    status: Optional[HospitalStatus] = None


class HospitalResponse(HospitalBase):
    hospital_id: int
    lab_id: int
    status: HospitalStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

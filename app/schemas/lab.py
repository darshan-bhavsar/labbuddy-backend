from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LabBase(BaseModel):
    name: str
    address: str
    contact_info: str
    url: str


class LabCreate(LabBase):
    admin_user_id: int


class LabUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_info: Optional[str] = None
    url: Optional[str] = None


class LabResponse(LabBase):
    lab_id: int
    admin_user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

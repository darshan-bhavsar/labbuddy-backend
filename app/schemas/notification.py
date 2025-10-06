from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.notification import NotificationStatus


class NotificationResponse(BaseModel):
    notification_id: int
    user_id: int
    report_id: Optional[int] = None
    message: str
    status: NotificationStatus
    sent_at: datetime

    class Config:
        from_attributes = True


class NotificationCreate(BaseModel):
    user_id: int
    report_id: Optional[int] = None
    message: str

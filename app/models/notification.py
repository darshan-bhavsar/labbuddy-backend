from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class NotificationStatus(str, enum.Enum):
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    report_id = Column(Integer, ForeignKey("reports.report_id"), nullable=True)
    message = Column(String(1000), nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.SENT)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    report = relationship("Report", back_populates="notifications")

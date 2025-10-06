from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Lab(Base):
    __tablename__ = "labs"

    lab_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=False)
    contact_info = Column(String(200), nullable=False)  # Phone, email, etc.
    url = Column(String(100), unique=True, index=True, nullable=False)  # Unique lab URL
    admin_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    admin_user = relationship("User", foreign_keys=[admin_user_id])
    users = relationship("User", back_populates="lab")
    hospitals = relationship("Hospital", back_populates="lab")
    patients = relationship("Patient", back_populates="lab")
    lab_tests = relationship("LabTest", back_populates="lab")
    reports = relationship("Report", back_populates="lab")

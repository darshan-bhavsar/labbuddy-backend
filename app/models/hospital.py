from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class HospitalStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Hospital(Base):
    __tablename__ = "hospitals"

    hospital_id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.lab_id"), nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(String(500), nullable=False)
    contact_info = Column(String(200), nullable=False)  # Phone, email, etc.
    status = Column(Enum(HospitalStatus), default=HospitalStatus.ACTIVE)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lab = relationship("Lab", back_populates="hospitals")
    users = relationship("User", back_populates="hospital")
    patients = relationship("Patient", back_populates="hospital")
    reports = relationship("Report", back_populates="hospital")

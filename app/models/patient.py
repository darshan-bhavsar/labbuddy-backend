from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.lab_id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"), nullable=True)
    name = Column(String(200), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    has_mediclaim = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lab = relationship("Lab", back_populates="patients")
    hospital = relationship("Hospital", back_populates="patients")
    reports = relationship("Report", back_populates="patient")

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class TestMaster(Base):
    __tablename__ = "test_masters"

    test_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    sample_type = Column(String(100), nullable=False)  # blood, urine, etc.
    turnaround_time = Column(Integer, nullable=False)  # hours
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lab_tests = relationship("LabTest", back_populates="test_master")


class LabTestStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class LabTest(Base):
    __tablename__ = "lab_tests"

    lab_test_id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.lab_id"), nullable=False)
    test_id = Column(Integer, ForeignKey("test_masters.test_id"), nullable=False)
    price = Column(Float, nullable=True)  # Optional pricing
    status = Column(Enum(LabTestStatus), default=LabTestStatus.ACTIVE)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lab = relationship("Lab", back_populates="lab_tests")
    test_master = relationship("TestMaster", back_populates="lab_tests")
    report_tests = relationship("ReportTest", back_populates="lab_test")

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..database import Base
from app.models.lab import Lab
from app.models.hospital import Hospital
from app.models.patient import Patient
from app.models.notification import Notification


class ReportStatus(str, enum.Enum):
    BOOKED = "BOOKED"
    SAMPLE_COLLECTED = "SAMPLE_COLLECTED"
    IN_PROCESS = "IN_PROCESS"
    REPORT_READY = "REPORT_READY"
    DELIVERED = "DELIVERED"


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.lab_id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"), nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    status = Column(Enum(ReportStatus), default=ReportStatus.BOOKED)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lab = relationship("Lab", back_populates="reports")
    hospital = relationship("Hospital", back_populates="reports")
    patient = relationship("Patient", back_populates="reports")
    report_tests = relationship("ReportTest", back_populates="report")
    report_files = relationship("ReportFile", back_populates="report")
    notifications = relationship("Notification", back_populates="report")


class ReportTestStatus(str, enum.Enum):
    IN_PROCESS = "IN_PROCESS"
    DONE = "DONE"


class ReportTest(Base):
    __tablename__ = "report_tests"

    report_test_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.report_id"), nullable=False)
    lab_test_id = Column(Integer, ForeignKey("lab_tests.lab_test_id"), nullable=False)
    result_value = Column(Text, nullable=True)  # Structured result if needed
    status = Column(Enum(ReportTestStatus), default=ReportTestStatus.IN_PROCESS)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    report = relationship("Report", back_populates="report_tests")
    lab_test = relationship("LabTest", back_populates="report_tests")


class ReportFile(Base):
    __tablename__ = "report_files"

    report_file_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.report_id"), nullable=False)
    file_url = Column(String(500), nullable=False)  # S3 URL or file path
    uploaded_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    is_signed = Column(Boolean, default=False)  # Digital signature status
    
    # Relationships
    report = relationship("Report", back_populates="report_files")
    uploaded_by_user = relationship("User", back_populates="uploaded_reports")

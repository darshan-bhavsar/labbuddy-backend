from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum
from ..database import Base


class UserRole(str, enum.Enum):
    LAB_ADMIN = "LAB_ADMIN"
    LAB_STAFF = "LAB_STAFF"
    LAB_BOY = "LAB_BOY"
    HOSPITAL_USER = "HOSPITAL_USER"
    PATIENT = "PATIENT"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
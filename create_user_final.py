#!/usr/bin/env python3
"""
Final script to create a test user for LabBuddy
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import hashlib
import enum

# Database setup
DATABASE_URL = "sqlite:///./labbuddy.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_test_user():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "admin@labbuddy.com").first()
        if existing_user:
            print("✅ User already exists!")
            print(f"Email: admin@labbuddy.com")
            print(f"Password: admin123")
            return
        
        # Create test user
        hashed_password = get_password_hash("admin123")
        user = User(
            name="Lab Admin",
            email="admin@labbuddy.com",
            password_hash=hashed_password,
            role=UserRole.LAB_ADMIN,
            is_active=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print("✅ Test user created successfully!")
        print(f"Email: admin@labbuddy.com")
        print(f"Password: admin123")
        print(f"Role: LAB_ADMIN")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()


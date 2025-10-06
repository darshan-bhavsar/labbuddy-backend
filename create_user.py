#!/usr/bin/env python3
"""
Script to create a test user for LabBuddy
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.utils.auth import get_password_hash
from app.database import Base

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

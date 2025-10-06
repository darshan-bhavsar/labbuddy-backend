from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.test import TestMaster, LabTest
from ..models.user import User
from ..schemas.test import TestMasterResponse, LabTestCreate, LabTestResponse
from ..utils.security import require_lab_admin

router = APIRouter(prefix="/tests", tags=["tests"])


@router.get("/master", response_model=List[TestMasterResponse])
def get_test_masters(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Get all available test masters."""
    tests = db.query(TestMaster).offset(skip).limit(limit).all()
    return tests


@router.get("/master/{test_id}", response_model=TestMasterResponse)
def get_test_master(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Get a specific test master by ID."""
    test = db.query(TestMaster).filter(TestMaster.test_id == test_id).first()
    if not test:
        raise HTTPException(
            status_code=404,
            detail="Test master not found"
        )
    return test


@router.post("/lab", response_model=LabTestResponse)
def create_lab_test(
    lab_test: LabTestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Add a test to a lab's available tests."""
    # Verify lab exists
    from ..models.lab import Lab
    lab = db.query(Lab).filter(Lab.lab_id == lab_test.lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=404,
            detail="Lab not found"
        )
    
    # Verify test master exists
    test_master = db.query(TestMaster).filter(TestMaster.test_id == lab_test.test_id).first()
    if not test_master:
        raise HTTPException(
            status_code=404,
            detail="Test master not found"
        )
    
    # Check if lab test already exists
    existing_lab_test = db.query(LabTest).filter(
        LabTest.lab_id == lab_test.lab_id,
        LabTest.test_id == lab_test.test_id
    ).first()
    if existing_lab_test:
        raise HTTPException(
            status_code=400,
            detail="Test already exists for this lab"
        )
    
    db_lab_test = LabTest(**lab_test.dict())
    db.add(db_lab_test)
    db.commit()
    db.refresh(db_lab_test)
    
    return db_lab_test


@router.get("/lab/{lab_id}", response_model=List[LabTestResponse])
def get_lab_tests(
    lab_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Get all tests available for a specific lab."""
    # Verify lab exists
    from ..models.lab import Lab
    lab = db.query(Lab).filter(Lab.lab_id == lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=404,
            detail="Lab not found"
        )
    
    lab_tests = db.query(LabTest).filter(
        LabTest.lab_id == lab_id
    ).offset(skip).limit(limit).all()
    
    return lab_tests


@router.put("/lab/{lab_test_id}", response_model=LabTestResponse)
def update_lab_test(
    lab_test_id: int,
    lab_test_update: LabTestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Update a lab test."""
    lab_test = db.query(LabTest).filter(LabTest.lab_test_id == lab_test_id).first()
    if not lab_test:
        raise HTTPException(
            status_code=404,
            detail="Lab test not found"
        )
    
    update_data = lab_test_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lab_test, field, value)
    
    db.commit()
    db.refresh(lab_test)
    
    return lab_test


@router.delete("/lab/{lab_test_id}")
def delete_lab_test(
    lab_test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Remove a test from a lab (soft delete by setting status to INACTIVE)."""
    lab_test = db.query(LabTest).filter(LabTest.lab_test_id == lab_test_id).first()
    if not lab_test:
        raise HTTPException(
            status_code=404,
            detail="Lab test not found"
        )
    
    from ..models.test import LabTestStatus
    lab_test.status = LabTestStatus.INACTIVE
    db.commit()
    
    return {"message": "Lab test removed successfully"}

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.hospital import Hospital
from ..models.user import User
from ..schemas.hospital import HospitalCreate, HospitalResponse, HospitalUpdate
from ..utils.security import require_lab_admin

router = APIRouter(prefix="/hospitals", tags=["hospitals"])


@router.post("/", response_model=HospitalResponse)
def create_hospital(
    hospital: HospitalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Create a new hospital (only lab admin can do this)."""
    # Verify lab exists
    from ..models.lab import Lab
    lab = db.query(Lab).filter(Lab.lab_id == hospital.lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=404,
            detail="Lab not found"
        )
    
    db_hospital = Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    
    return db_hospital


@router.get("/", response_model=List[HospitalResponse])
def get_hospitals(
    lab_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Get hospitals, optionally filtered by lab_id."""
    query = db.query(Hospital)
    
    if lab_id:
        query = query.filter(Hospital.lab_id == lab_id)
    
    hospitals = query.offset(skip).limit(limit).all()
    return hospitals


@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Get a specific hospital by ID."""
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )
    return hospital


@router.put("/{hospital_id}", response_model=HospitalResponse)
def update_hospital(
    hospital_id: int,
    hospital_update: HospitalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Update a hospital."""
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )
    
    update_data = hospital_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(hospital, field, value)
    
    db.commit()
    db.refresh(hospital)
    
    return hospital


@router.delete("/{hospital_id}")
def delete_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Delete a hospital (soft delete by setting status to INACTIVE)."""
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )
    
    from ..models.hospital import HospitalStatus
    hospital.status = HospitalStatus.INACTIVE
    db.commit()
    
    return {"message": "Hospital deleted successfully"}

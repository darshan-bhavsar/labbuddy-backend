from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.lab import Lab
from ..models.user import User
from ..schemas.lab import LabCreate, LabResponse, LabUpdate
from ..utils.security import require_lab_admin

router = APIRouter(prefix="/labs", tags=["labs"])


@router.post("/", response_model=LabResponse)
def create_lab(
    lab: LabCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Create a new lab (only lab admin can do this)."""
    # Check if URL is already taken
    existing_lab = db.query(Lab).filter(Lab.url == lab.url).first()
    if existing_lab:
        raise HTTPException(
            status_code=400,
            detail="Lab URL already exists"
        )
    
    # Verify admin user exists
    admin_user = db.query(User).filter(User.user_id == lab.admin_user_id).first()
    if not admin_user:
        raise HTTPException(
            status_code=404,
            detail="Admin user not found"
        )
    
    db_lab = Lab(**lab.dict())
    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)
    
    return db_lab


@router.get("/", response_model=List[LabResponse])
def get_labs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Get all labs (only lab admin can access)."""
    labs = db.query(Lab).offset(skip).limit(limit).all()
    return labs


@router.get("/{lab_id}", response_model=LabResponse)
def get_lab(
    lab_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Get a specific lab by ID."""
    lab = db.query(Lab).filter(Lab.lab_id == lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=404,
            detail="Lab not found"
        )
    return lab


@router.put("/{lab_id}", response_model=LabResponse)
def update_lab(
    lab_id: int,
    lab_update: LabUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Update a lab."""
    lab = db.query(Lab).filter(Lab.lab_id == lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=404,
            detail="Lab not found"
        )
    
    # Check if new URL is already taken (if provided)
    if lab_update.url and lab_update.url != lab.url:
        existing_lab = db.query(Lab).filter(Lab.url == lab_update.url).first()
        if existing_lab:
            raise HTTPException(
                status_code=400,
                detail="Lab URL already exists"
            )
    
    update_data = lab_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lab, field, value)
    
    db.commit()
    db.refresh(lab)
    
    return lab


@router.delete("/{lab_id}")
def delete_lab(
    lab_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_admin)
):
    """Delete a lab (soft delete by setting is_active to False)."""
    lab = db.query(Lab).filter(Lab.lab_id == lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=404,
            detail="Lab not found"
        )
    
    lab.is_active = False
    db.commit()
    
    return {"message": "Lab deleted successfully"}

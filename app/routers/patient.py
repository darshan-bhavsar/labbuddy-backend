from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.patient import Patient
from ..models.user import User
from ..schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from ..utils.security import require_lab_staff

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Create a new patient."""
    # Verify lab exists
    from ..models.lab import Lab
    lab = db.query(Lab).filter(Lab.lab_id == patient.lab_id).first()
    if not lab:
        raise HTTPException(
            status_code=404,
            detail="Lab not found"
        )
    
    # Verify hospital exists if provided
    if patient.hospital_id:
        from ..models.hospital import Hospital
        hospital = db.query(Hospital).filter(Hospital.hospital_id == patient.hospital_id).first()
        if not hospital:
            raise HTTPException(
                status_code=404,
                detail="Hospital not found"
            )
    
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return db_patient


@router.get("/", response_model=List[PatientResponse])
def get_patients(
    lab_id: int = None,
    hospital_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Get patients, optionally filtered by lab_id or hospital_id."""
    query = db.query(Patient)
    
    if lab_id:
        query = query.filter(Patient.lab_id == lab_id)
    if hospital_id:
        query = query.filter(Patient.hospital_id == hospital_id)
    
    patients = query.offset(skip).limit(limit).all()
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Get a specific patient by ID."""
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Update a patient."""
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    
    # Verify hospital exists if provided
    if patient_update.hospital_id:
        from ..models.hospital import Hospital
        hospital = db.query(Hospital).filter(Hospital.hospital_id == patient_update.hospital_id).first()
        if not hospital:
            raise HTTPException(
                status_code=404,
                detail="Hospital not found"
            )
    
    update_data = patient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    db.commit()
    db.refresh(patient)
    
    return patient


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_lab_staff)
):
    """Delete a patient."""
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    
    db.delete(patient)
    db.commit()
    
    return {"message": "Patient deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

import schemas
from auth import get_current_user
from database import get_db, SQLiteDB

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=list[schemas.PatientOut])
def list_patients(
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    patients = list(db.patients.find({"user_id": str(current_user["_id"])}).sort("_id", -1))
    return patients


@router.post("", response_model=schemas.PatientOut)
def create_patient(
    payload: schemas.PatientCreate,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    patient_dict = payload.model_dump()
    patient_dict["user_id"] = str(current_user["_id"])
    patient_dict["created_at"] = datetime.utcnow()
    result = db.patients.insert_one(patient_dict)
    patient_dict["_id"] = result.inserted_id
    return patient_dict


@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(
    patient_id: str,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    patient = db.patients.find_one({"_id": patient_id, "user_id": str(current_user["_id"])})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=schemas.PatientOut)
def update_patient(
    patient_id: str,
    payload: schemas.PatientUpdate,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    patient = db.patients.find_one({"_id": patient_id, "user_id": str(current_user["_id"])})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if update_data:
        db.patients.update_one({"_id": patient_id}, {"$set": update_data})
        patient.update(update_data)

    return patient


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: str,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = db.patients.delete_one({"_id": patient_id, "user_id": str(current_user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"success": True}

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

import schemas
from auth import create_access_token, get_password_hash, verify_password
from database import get_db, SQLiteDB

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut)
def register(payload: schemas.UserCreate, db: SQLiteDB = Depends(get_db)):
    normalized_email = payload.email.lower().strip()
    existing = db.users.find_one({"email": normalized_email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user_doc = {
        "name": payload.name.strip(),
        "email": normalized_email,
        "password_hash": get_password_hash(payload.password),
        "role": "doctor",
        "created_at": datetime.utcnow()
    }
    result = db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return user_doc


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.LoginRequest, db: SQLiteDB = Depends(get_db)):
    user = db.users.find_one({"email": payload.email.lower().strip()})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(str(user["_id"]))
    return schemas.Token(access_token=token)

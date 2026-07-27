"""
Admin Routes — accessible only to users with role='admin'.

Endpoints:
  GET    /api/admin/stats              – System-wide statistics
  GET    /api/admin/users              – List all users (doctors + admins)
  POST   /api/admin/users              – Create a new user
  PUT    /api/admin/users/{id}         – Update user name / role
  DELETE /api/admin/users/{id}         – Delete a user
  GET    /api/admin/patients           – All patients across all doctors
  DELETE /api/admin/patients/{id}      – Delete any patient
  GET    /api/admin/foods              – All foods (same as public but no limit)
  POST   /api/admin/foods              – Add a new food
  PUT    /api/admin/foods/{id}         – Edit a food
  DELETE /api/admin/foods/{id}         – Delete a food
  GET    /api/admin/diet-plans         – All diet plans across all users
  DELETE /api/admin/diet-plans/{id}    – Delete any diet plan
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from auth import get_admin_user, get_password_hash
from database import get_db, SQLiteDB

router = APIRouter(prefix="/api/admin", tags=["admin"])


# ─── helpers ────────────────────────────────────────────────────────────────

def _str_ids(doc: dict) -> dict:
    """Recursively convert _id fields to strings for JSON serialisation."""
    if doc is None:
        return doc
    doc["id"] = str(doc.pop("_id", ""))
    return doc


# ─── Stats ──────────────────────────────────────────────────────────────────

@router.get("/stats")
def get_stats(
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    """Return high-level platform statistics."""
    total_users    = db.users.count_documents({})
    total_doctors  = db.users.count_documents({"role": "doctor"})
    total_admins   = db.users.count_documents({"role": "admin"})
    total_patients = db.patients.count_documents({})
    total_plans    = db.diet_plans.count_documents({})
    total_foods    = db.foods.count_documents({})

    # Patients per vikriti
    vikriti_pipeline = [
        {"$group": {"_id": "$vikriti", "count": {"$sum": 1}}}
    ]
    vikriti_breakdown = {
        item["_id"]: item["count"]
        for item in db.patients.aggregate(vikriti_pipeline)
        if item["_id"]
    }

    # Plans and patients in last 7 days
    from datetime import timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_plans    = db.diet_plans.count_documents(
        {"created_at": {"$gte": seven_days_ago}}
    )
    recent_patients = db.patients.count_documents(
        {"created_at": {"$gte": seven_days_ago}}
    )

    return {
        "users": {
            "total": total_users,
            "doctors": total_doctors,
            "admins": total_admins,
        },
        "patients": {
            "total": total_patients,
            "last_7_days": recent_patients,
            "vikriti_breakdown": vikriti_breakdown,
        },
        "diet_plans": {
            "total": total_plans,
            "last_7_days": recent_plans,
        },
        "foods": {
            "total": total_foods,
        },
    }


# ─── User Management ────────────────────────────────────────────────────────

@router.get("/users")
def list_users(
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    users = list(db.users.find({}, {"password_hash": 0}).sort("created_at", -1))
    for u in users:
        u["id"] = str(u.pop("_id"))
    return users


@router.post("/users", status_code=201)
def create_user(
    payload: dict,
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    """Create a doctor or admin account."""
    email = (payload.get("email") or "").lower().strip()
    if not email or not payload.get("password") or not payload.get("name"):
        raise HTTPException(status_code=422, detail="name, email and password are required")

    if db.users.find_one({"email": email}):
        raise HTTPException(status_code=409, detail="Email already registered")

    role = payload.get("role", "doctor")
    if role not in ("doctor", "admin"):
        raise HTTPException(status_code=422, detail="role must be 'doctor' or 'admin'")

    user_doc = {
        "name": payload["name"].strip(),
        "email": email,
        "password_hash": get_password_hash(payload["password"]),
        "role": role,
        "created_at": datetime.utcnow(),
    }
    result = db.users.insert_one(user_doc)
    user_doc["id"] = str(result.inserted_id)
    user_doc.pop("password_hash", None)
    user_doc.pop("_id", None)
    return user_doc


@router.put("/users/{user_id}")
def update_user(
    user_id: str,
    payload: dict,
    db: SQLiteDB = Depends(get_db),
    admin: dict = Depends(get_admin_user),
):
    """Update a user's name or role. Cannot demote yourself."""
    if user_id == str(admin["_id"]) and payload.get("role") != "admin":
        raise HTTPException(status_code=400, detail="Cannot demote your own admin account")

    update = {}
    if "name" in payload:
        update["name"] = payload["name"].strip()
    if "role" in payload:
        if payload["role"] not in ("doctor", "admin"):
            raise HTTPException(status_code=422, detail="role must be 'doctor' or 'admin'")
        update["role"] = payload["role"]
    if "password" in payload and payload["password"]:
        update["password_hash"] = get_password_hash(payload["password"])

    if not update:
        raise HTTPException(status_code=422, detail="No valid fields to update")

    result = db.users.update_one({"_id": user_id}, {"$set": update})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    user = db.users.find_one({"_id": user_id}, {"password_hash": 0})
    user["id"] = str(user.pop("_id"))
    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    db: SQLiteDB = Depends(get_db),
    admin: dict = Depends(get_admin_user),
):
    """Delete a user. Cannot delete yourself."""
    if user_id == str(admin["_id"]):
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    result = db.users.delete_one({"_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "deleted_id": user_id}


# ─── Patient Management ─────────────────────────────────────────────────────

@router.get("/patients")
def list_all_patients(
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    """Return all patients across all doctors."""
    patients = list(db.patients.find().sort("created_at", -1))
    for p in patients:
        p["id"] = str(p.pop("_id"))
    return patients


@router.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: str,
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    result = db.patients.delete_one({"_id": patient_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    # Also remove their plans
    db.diet_plans.delete_many({"patient_id": patient_id})
    return {"success": True}


# ─── Food Management ────────────────────────────────────────────────────────

@router.get("/foods")
def list_all_foods(
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    foods = list(db.foods.find().sort("name", 1))
    for f in foods:
        f["id"] = str(f.pop("_id"))
    return foods


@router.post("/foods", status_code=201)
def create_food(
    payload: dict,
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    """Add a new food to the database."""
    if not payload.get("name") or not payload.get("category"):
        raise HTTPException(status_code=422, detail="name and category are required")

    if db.foods.find_one({"name": payload["name"]}):
        raise HTTPException(status_code=409, detail="Food with this name already exists")

    food_doc = {
        "name": payload["name"],
        "name_hindi": payload.get("name_hindi"),
        "category": payload["category"],
        "subcategory": payload.get("subcategory"),
        "calories": float(payload.get("calories", 0)),
        "protein_g": float(payload.get("protein_g", 0)),
        "carbs_g": float(payload.get("carbs_g", 0)),
        "fat_g": float(payload.get("fat_g", 0)),
        "fiber_g": float(payload.get("fiber_g", 0)),
        "rasa": payload.get("rasa"),
        "virya": payload.get("virya"),
        "vipaka": payload.get("vipaka"),
        "vata_effect": int(payload.get("vata_effect", 0)),
        "pitta_effect": int(payload.get("pitta_effect", 0)),
        "kapha_effect": int(payload.get("kapha_effect", 0)),
        "is_pathya_for": payload.get("is_pathya_for", []),
        "is_apathya_for": payload.get("is_apathya_for", []),
        "is_vegetarian": bool(payload.get("is_vegetarian", True)),
        "season_best": payload.get("season_best"),
        "description": payload.get("description"),
    }
    result = db.foods.insert_one(food_doc)
    food_doc["id"] = str(result.inserted_id)
    food_doc.pop("_id", None)
    return food_doc


@router.put("/foods/{food_id}")
def update_food(
    food_id: str,
    payload: dict,
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    """Edit any field of a food."""
    allowed_fields = {
        "name", "name_hindi", "category", "subcategory", "calories",
        "protein_g", "carbs_g", "fat_g", "fiber_g", "rasa", "virya",
        "vipaka", "vata_effect", "pitta_effect", "kapha_effect",
        "is_pathya_for", "is_apathya_for", "is_vegetarian",
        "season_best", "description",
    }
    update = {k: v for k, v in payload.items() if k in allowed_fields}
    if not update:
        raise HTTPException(status_code=422, detail="No valid fields provided")

    result = db.foods.update_one({"_id": food_id}, {"$set": update})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Food not found")

    food = db.foods.find_one({"_id": food_id})
    food["id"] = str(food.pop("_id"))
    return food


@router.delete("/foods/{food_id}")
def delete_food(
    food_id: str,
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    result = db.foods.delete_one({"_id": food_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Food not found")
    return {"success": True}


# ─── Diet Plan Management ───────────────────────────────────────────────────

@router.get("/diet-plans")
def list_all_plans(
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    """All diet plans across all users (without embedded items for performance)."""
    plans = list(db.diet_plans.find({}, {"items": 0}).sort("created_at", -1).limit(500))
    for p in plans:
        p["id"] = str(p.pop("_id"))
    return plans


@router.delete("/diet-plans/{plan_id}")
def delete_plan(
    plan_id: str,
    db: SQLiteDB = Depends(get_db),
    _admin: dict = Depends(get_admin_user),
):
    result = db.diet_plans.delete_one({"_id": plan_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"success": True}

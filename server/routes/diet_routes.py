from fastapi import APIRouter, Depends, HTTPException

import schemas
from auth import get_current_user
from database import get_db, SQLiteDB
from engine.ayur_logic import generate_plan

router = APIRouter(tags=["diet"])


def _format_plan(plan: dict) -> dict:
    plan["id"] = str(plan["_id"])
    for item in plan.get("items", []):
        if "_id" in item:
            item["id"] = str(item["_id"])
        if "food" in item and "_id" in item["food"]:
            item["food"]["id"] = str(item["food"]["_id"])
    return plan


@router.get("/api/templates", response_model=list[schemas.TemplateOut])
def list_templates(
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _ = current_user
    templates = list(db.diet_templates.find().sort("_id", 1))
    for t in templates:
        t["id"] = str(t["_id"])
    return templates


@router.get("/api/diet-plans", response_model=list[schemas.DietPlanOut])
def list_diet_plans(
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    plans = list(db.diet_plans.find({"user_id": str(current_user["_id"])}).sort("created_at", -1))
    return [_format_plan(p) for p in plans]


@router.post("/api/diet-plans/generate", response_model=schemas.DietPlanOut)
def create_plan(
    payload: schemas.DietPlanGenerateRequest,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    patient = db.patients.find_one({"_id": payload.patient_id, "user_id": str(current_user["_id"])})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    template = db.diet_templates.find_one({"_id": payload.template_id})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    plan = generate_plan(db, patient, current_user, template)
    return _format_plan(plan)


@router.get("/api/diet-plans/{plan_id}", response_model=schemas.DietPlanOut)
def get_plan(
    plan_id: str,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    plan = db.diet_plans.find_one({"_id": plan_id, "user_id": str(current_user["_id"])})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _format_plan(plan)


@router.get("/api/diet-plans/patient/{patient_id}", response_model=list[schemas.DietPlanOut])
def list_plans_for_patient(
    patient_id: str,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    plans = list(db.diet_plans.find({
        "patient_id": patient_id,
        "user_id": str(current_user["_id"])
    }).sort("_id", -1))
    return [_format_plan(p) for p in plans]


@router.put("/api/diet-plans/{plan_id}", response_model=schemas.DietPlanOut)
def update_plan(
    plan_id: str,
    payload: schemas.DietPlanUpdate,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    plan = db.diet_plans.find_one({"_id": plan_id, "user_id": str(current_user["_id"])})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    update_fields = {}
    if payload.notes is not None:
        update_fields["notes"] = payload.notes
    if payload.target_calories is not None:
        update_fields["target_calories"] = payload.target_calories
    if payload.target_protein is not None:
        update_fields["target_protein"] = payload.target_protein
    if payload.target_carbs is not None:
        update_fields["target_carbs"] = payload.target_carbs
    if payload.target_fat is not None:
        update_fields["target_fat"] = payload.target_fat

    if update_fields:
        db.diet_plans.update_one({"_id": plan_id}, {"$set": update_fields})
        plan.update(update_fields)

    # Update embedded items
    if payload.items:
        for item_update in payload.items:
            for item in plan.get("items", []):
                if str(item.get("id", "")) == str(item_update.id) or str(item.get("_id", "")) == str(item_update.id):
                    food = db.foods.find_one({"_id": item_update.food_id})
                    if food:
                        factor = item_update.portion_g / 100.0
                        item["food_id"] = str(food["_id"])
                        item["food"] = food
                        item["portion_g"] = item_update.portion_g
                        item["calories"] = round(food["calories"] * factor, 2)
                        item["protein"] = round(food["protein_g"] * factor, 2)
                        item["carbs"] = round(food["carbs_g"] * factor, 2)
                        item["fat"] = round(food["fat_g"] * factor, 2)

        plan["total_calories"] = round(sum(i.get("calories", 0) for i in plan.get("items", [])), 2)
        plan["total_protein"] = round(sum(i.get("protein", 0) for i in plan.get("items", [])), 2)
        plan["total_carbs"] = round(sum(i.get("carbs", 0) for i in plan.get("items", [])), 2)
        plan["total_fat"] = round(sum(i.get("fat", 0) for i in plan.get("items", [])), 2)

        db.diet_plans.update_one({"_id": plan_id}, {"$set": {
            "items": plan["items"],
            "total_calories": plan["total_calories"],
            "total_protein": plan["total_protein"],
            "total_carbs": plan["total_carbs"],
            "total_fat": plan["total_fat"],
        }})

    return _format_plan(plan)

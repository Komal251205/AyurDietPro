from fastapi import APIRouter, Depends, HTTPException
import re

import schemas
from auth import get_current_user
from database import get_db, SQLiteDB

router = APIRouter(prefix="/api/foods", tags=["foods"])


@router.get("", response_model=list[schemas.FoodOut])
def list_foods(
    q: str | None = None,
    category: str | None = None,
    vegetarian: bool | None = None,
    vikriti: str | None = None,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _ = current_user
    filter_query: dict = {}

    if q:
        filter_query["name"] = {"$regex": re.escape(q), "$options": "i"}
    if category:
        filter_query["category"] = category
    if vegetarian is not None:
        filter_query["is_vegetarian"] = vegetarian

    if vikriti:
        v = vikriti.lower()
        if v == "vata":
            filter_query["vata_effect"] = {"$lte": 0}
        elif v == "pitta":
            filter_query["pitta_effect"] = {"$lte": 0}
        elif v == "kapha":
            filter_query["kapha_effect"] = {"$lte": 0}

    foods = list(db.foods.find(filter_query).sort("name", 1).limit(200))
    return foods


@router.get("/categories", response_model=list[str])
def list_categories(
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _ = current_user
    return sorted(db.foods.distinct("category"))


@router.get("/{food_id}", response_model=schemas.FoodOut)
def get_food(
    food_id: str,
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    _ = current_user
    food = db.foods.find_one({"_id": food_id})
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food

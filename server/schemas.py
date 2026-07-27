from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    role: str


class PatientBase(BaseModel):
    name: str
    phone: Optional[str] = None
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    activity_level: str
    vikriti: str
    prakriti: str
    conditions: list[str] = []
    appetite: str
    digestion_strength: str
    food_preference: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    activity_level: Optional[str] = None
    vikriti: Optional[str] = None
    prakriti: Optional[str] = None
    conditions: Optional[list[str]] = None
    appetite: Optional[str] = None
    digestion_strength: Optional[str] = None
    food_preference: Optional[str] = None


class PatientOut(PatientBase):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(alias="_id", default=None)
    user_id: str
    created_at: datetime


class FoodOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    name_hindi: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    rasa: Optional[str] = None
    virya: Optional[str] = None
    vipaka: Optional[str] = None
    vata_effect: int
    pitta_effect: int
    kapha_effect: int
    is_pathya_for: list[str] = []
    is_apathya_for: list[str] = []
    is_vegetarian: bool
    season_best: Optional[str] = None
    description: Optional[str] = None


class TemplateOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    target_vikriti: str
    goal: str
    description: Optional[str] = None
    meal_slots: dict[str, Any]


class DietPlanGenerateRequest(BaseModel):
    patient_id: str
    template_id: str


class DietPlanItemUpdate(BaseModel):
    id: str
    food_id: str
    portion_g: float


class DietPlanUpdate(BaseModel):
    notes: Optional[str] = None
    target_calories: Optional[float] = None
    target_protein: Optional[float] = None
    target_carbs: Optional[float] = None
    target_fat: Optional[float] = None
    items: list[DietPlanItemUpdate] = []


class DietPlanItemOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(alias="_id", default=None)
    food_id: str
    meal_slot: str
    day_of_week: int
    portion_g: float
    calories: float
    protein: float
    carbs: float
    fat: float
    reasoning: Optional[str] = None
    is_conflict: bool
    food: FoodOut


class DietPlanOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(alias="_id", default=None)
    patient_id: str
    user_id: str
    template_id: Optional[str] = None
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    target_calories: float
    target_protein: float
    target_carbs: float
    target_fat: float
    notes: Optional[str] = None
    created_at: datetime
    items: list[DietPlanItemOut]

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from auth import get_current_user
from database import get_db, SQLiteDB

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/weekly")
def get_weekly_report(
    db: SQLiteDB = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    user_id_str = str(current_user["_id"])

    # New patients in last 7 days
    new_patients_count = db.patients.count_documents({
        "user_id": user_id_str,
        "created_at": {"$gte": seven_days_ago}
    })

    # Diet plans in last 7 days
    new_plans_count = db.diet_plans.count_documents({
        "user_id": user_id_str,
        "created_at": {"$gte": seven_days_ago}
    })

    # Patient distribution by Vikriti
    pipeline = [
        {"$match": {"user_id": user_id_str}},
        {"$group": {"_id": "$vikriti", "count": {"$sum": 1}}}
    ]
    vikriti_dist = list(db.patients.aggregate(pipeline))
    vikriti_stats = {item["_id"]: item["count"] for item in vikriti_dist if item["_id"]}

    # Recent patients
    recent_patients = list(db.patients.find(
        {"user_id": user_id_str}
    ).sort("created_at", -1).limit(5))

    return {
        "stats": {
            "new_patients": new_patients_count,
            "new_plans": new_plans_count,
            "vikriti_breakdown": vikriti_stats,
        },
        "recent_patients": [
            {
                "id": str(p["_id"]),
                "name": p.get("name"),
                "vikriti": p.get("vikriti"),
                "created_at": p.get("created_at")
            }
            for p in recent_patients
        ],
    }

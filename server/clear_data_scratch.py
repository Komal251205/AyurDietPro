import sys
import os

# Add the parent directory to sys.path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Patient, DietPlan, DietPlanItem

def clear_data():
    db = SessionLocal()
    try:
        # Delete in order of dependency
        print("Deleting diet plan items...")
        db.query(DietPlanItem).delete()
        
        print("Deleting diet plans...")
        db.query(DietPlan).delete()
        
        print("Deleting patients...")
        db.query(Patient).delete()
        
        db.commit()
        print("Successfully reset all patient and chart counts to zero.")
    except Exception as e:
        db.rollback()
        print(f"Error resetting data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_data()

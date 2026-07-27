import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function PatientViewPage() {
  const { id } = useParams();
  const [plan, setPlan] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/public/plan/${id}`)
      .then((res) => (res.ok ? res.json() : Promise.reject()))
      .then(setPlan)
      .catch(() => setPlan(null));
  }, [id]);

  if (!plan) {
    return <div className="container card">Loading plan...</div>;
  }

  return (
    <div className="container card">
      <h2>Daily Diet Schedule</h2>
      {plan.items.map((item) => (
        <div key={item.id} className="line">
          <strong>{item.meal_slot}</strong>: {item.food.name} - {item.portion_g} g
        </div>
      ))}
      <p className="muted">
        Total: {plan.total_calories} kcal | P {plan.total_protein} | C {plan.total_carbs} | F {plan.total_fat}
      </p>
    </div>
  );
}


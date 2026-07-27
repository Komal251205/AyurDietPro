export default function NutritionBar({ plan }) {
  if (!plan) return null;

  const stats = [
    { label: "Calories", actual: plan.total_calories, target: plan.target_calories, unit: "kcal", class: "calories" },
    { label: "Protein", actual: plan.total_protein, target: plan.target_protein, unit: "g", class: "protein" },
    { label: "Carbs", actual: plan.total_carbs, target: plan.target_carbs, unit: "g", class: "carbs" },
    { label: "Fat", actual: plan.total_fat, target: plan.target_fat, unit: "g", class: "fat" },
  ];

  return (
    <div className="card">
      <div className="target-dashboard">
        {stats.map((s) => {
          const percent = Math.min((s.actual / s.target) * 100, 100);
          const isOver = s.actual > s.target;
          return (
            <div key={s.label} className="gauge-wrap">
              <div className="gauge-label">
                <span>{s.label}</span>
                <span className={isOver ? "over-target" : ""}>
                  {s.actual} / {s.target} {s.unit}
                </span>
              </div>
              <div className="gauge-track">
                <div className={`gauge-fill ${s.class}`} style={{ width: `${percent}%` }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}


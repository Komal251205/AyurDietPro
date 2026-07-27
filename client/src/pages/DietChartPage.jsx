import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import FoodSearchDropdown from "../components/FoodSearchDropdown";
import MealCard from "../components/MealCard";
import NutritionBar from "../components/NutritionBar";
import ReasoningModal from "../components/ReasoningModal";
import { exportDietPlanPdf } from "../utils/pdfExport";

export default function DietChartPage() {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);
  const [templates, setTemplates] = useState([]);
  const [templateId, setTemplateId] = useState("");
  const [plan, setPlan] = useState(null);
  const [foods, setFoods] = useState([]);
  const [selectedDay, setSelectedDay] = useState(1);
  const [openReasoning, setOpenReasoning] = useState(false);

  useEffect(() => {
    api.patient(id).then(setPatient);
    api.templates().then((t) => {
      setTemplates(t);
      if (t[0]) setTemplateId(String(t[0].id));
    });
    api.foods().then(setFoods);
    api.patientPlans(id).then((plans) => {
      if (plans && plans.length > 0) {
        setPlan(plans[0]); // Load the most recent plan
      }
    });
  }, [id]);

  const updateItem = async (item, foodId, portionG) => {
    if (!plan) return;
    const updated = await api.updatePlan(plan.id, {
      items: [{ id: item.id, food_id: foodId || item.food_id, portion_g: portionG || item.portion_g }],
    });
    setPlan(updated);
  };

  const updateTargets = async (targets) => {
    if (!plan) return;
    const updated = await api.updatePlan(plan.id, targets);
    setPlan(updated);
  };

  const generate = async () => {
    const generated = await api.generatePlan({ patient_id: Number(id), template_id: Number(templateId) });
    setPlan(generated);
  };

  const dayItems = useMemo(() => {
    if (!plan) return [];
    return plan.items.filter((i) => i.day_of_week === selectedDay);
  }, [plan, selectedDay]);

  return (
    <div className="container">
      <div className="card">
        <div className="spread">
          <div>
            <h1>Diet Chart Builder</h1>
            <p className="muted">Craft a balanced, clinical-grade plan for {patient?.name}.</p>
          </div>
          <div className="row">
            {plan && patient && (
              <button className="primary-btn" onClick={() => exportDietPlanPdf(patient, plan)}>
                PDF Export
              </button>
            )}
            {plan && (
              <button className="ghost-btn" onClick={() => setOpenReasoning(true)}>
                Ayur-Logic Reasoning
              </button>
            )}
          </div>
        </div>

        <div className="row" style={{ marginTop: "1rem" }}>
          <select value={templateId} onChange={(e) => setTemplateId(e.target.value)}>
            {templates.map((template) => (
              <option key={template.id} value={template.id}>
                Template: {template.name}
              </option>
            ))}
          </select>
          <button className="primary-btn" onClick={generate} disabled={!templateId}>
            {plan ? "Re-Generate Plan" : "Generate Initial Plan"}
          </button>
        </div>
      </div>

      {plan && (
        <>
          <div className="day-switcher">
            {[1, 2, 3, 4, 5, 6, 7].map((day) => (
              <button
                key={day}
                className={`day-btn ${selectedDay === day ? "active" : ""}`}
                onClick={() => setSelectedDay(day)}
              >
                Day {day}
              </button>
            ))}
          </div>

          <NutritionBar plan={plan} />

          <div className="card">
            <div className="spread" style={{ marginBottom: "1rem" }}>
              <h2>Meals - Day {selectedDay}</h2>
              <div className="row">
                <div className="form-group">
                  <label style={{ fontSize: "0.7rem" }}>TARGET CALORIES</label>
                  <input
                    type="number"
                    value={plan.target_calories}
                    onChange={(e) => updateTargets({ target_calories: Number(e.target.value) })}
                    style={{ width: "100px", padding: "4px 8px" }}
                  />
                </div>
              </div>
            </div>

            {dayItems.length === 0 && (
              <div className="muted" style={{ padding: "2rem", textAlign: "center" }}>
                No items generated for this day. Use a weekly template or add items manually.
              </div>
            )}

            <div className="form-grid">
              {dayItems.map((item) => (
                <MealCard
                  key={item.id}
                  item={item}
                  onPortionChange={(newPortion) => updateItem(item, null, newPortion)}
                  actions={
                    <FoodSearchDropdown
                      foods={foods}
                      value={item.food_id}
                      onChange={(foodId) => updateItem(item, foodId, null)}
                    />
                  }
                />
              ))}
            </div>
          </div>

          <div style={{ marginTop: "2rem", display: "flex", justifyContent: "center" }}>
            <Link className="primary-btn" to={`/plan/${plan.id}/view`} style={{ padding: "12px 32px" }}>
              Launch Interactive Patient View
            </Link>
          </div>
        </>
      )}
      <ReasoningModal open={openReasoning} onClose={() => setOpenReasoning(false)} items={plan?.items || []} />
    </div>
  );
}


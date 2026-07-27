import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export function exportDietPlanPdf(patient, plan) {
  const doc = new jsPDF();
  doc.setFontSize(18);
  doc.text("AyurDiet Pro", 14, 15);
  doc.setFontSize(11);
  doc.text(`Patient: ${patient.name}`, 14, 24);
  doc.text(`Phone: ${patient.phone || "N/A"}`, 14, 30);
  doc.text(`Vikriti: ${patient.vikriti}`, 14, 36);

  autoTable(doc, {
    startY: 42,
    head: [["Meal", "Food", "Portion (g)", "Calories", "Conflict"]],
    body: plan.items.map((item) => [
      item.meal_slot,
      item.food.name,
      String(item.portion_g),
      String(item.calories),
      item.is_conflict ? "Yes" : "No",
    ]),
  });

  const y = doc.lastAutoTable.finalY + 10;
  doc.text(
    `Totals: ${plan.total_calories} kcal | P ${plan.total_protein}g | C ${plan.total_carbs}g | F ${plan.total_fat}g`,
    14,
    y
  );
  doc.save(`diet-plan-${patient.name}.pdf`);
}


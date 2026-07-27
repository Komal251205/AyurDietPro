# AyurDiet Pro: Clinical Methodology & Logic 🧪

This document provides an in-depth explanation of the algorithms and clinical frameworks that power AyurDiet Pro. The system is built on a hybrid architecture that validates classic Ayurvedic "Pathya" (compatible) principles against modern dietetic standards.

---

## 🚀 Step-by-Step Automation Workflow

The "Generate" process follows a prioritized algorithmic pipeline to transform patient data into a clinical chart:

1.  **Macro-Target Baselining**: The system calculates the patient's **BMR** (Mifflin-St Jeor) and **TDEE**, then derives a daily target of **55% Carbs, 20% Protein, and 25% Fat**.
2.  **Therapeutic Filtering**: 
    - **Dosha Balancing**: It filters the database for foods that "Pacify" (reduce) the patient's current Vikriti.
    - **Thermal Check**: It aligns the food's **Virya** (Potency) with the clinical goal (e.g., cooling foods for High Pitta).
3.  **Template Application**: It applies category priorities from the selected **Diet Template** (e.g., "Weight Loss" prioritizing specific vegetables and pulses).
4.  **7-Day Scheduling**: 
    - It loops through 7 days, identifying a fresh pool of compatible items for each meal slot.
    - It applies **Intelligent Randomization** within that pool to ensure daily variety while maintaining clinical integrity.
5.  **Automated Portioning**: It auto-calculates the exact **Portion (g)** for each meal to meet the caloric and macro targets precisely.
6.  **Conflict (Apathya) Guard**: It runs a final real-time check against the patient's medical history to flag any contraindicated foods.

---

## 1. Nutritional Foundation: Quantitative Analysis

The primary layer of the diet generation engine ensures that every patient meets their physiological energy requirements.

### Basal Metabolic Rate (BMR)
We utilize the **Mifflin-St Jeor Equation**, currently considered the most accurate for healthy individuals in a clinical setting.

- **For Men**: $BMR = (10 \times weight\text{ in kg}) + (6.25 \times height\text{ in cm}) - (5 \times age\text{ in years}) + 5$
- **For Women**: $BMR = (10 \times weight\text{ in kg}) + (6.25 \times height\text{ in cm}) - (5 \times age\text{ in years}) - 161$

### Total Daily Energy Expenditure (TDEE)
The BMR is adjusted using a **PAL (Physical Activity Level)** multiplier:
- **Sedentary**: 1.2
- **Lightly Active**: 1.375
- **Moderately Active**: 1.55
- **Very Active**: 1.725
- **Extremely Active**: 1.9

### Macro-Nutrient Distribution
The target macros are determined by a standard clinical split designed for metabolic stability:
- **Carbohydrates (55%)**: Primary energy source.
- **Protein (20%)**: Support for muscle mass and repair.
- **Fat (25%)**: Essential for hormone regulation and fat-soluble vitamin absorption.

---

## 2. Ayurvedic Engine: Qualitative Rebalancing

Once the quantitative targets are set, the "Ayur-Logic" engine filters candidates based on their impact on the patient's **Vikriti** (current imbalance).

### The Three Doshas
The engine performs a weighted analysis of food impacts:
- **Vata (Air/Ether)**: Grounding, warm, and moistening foods are prioritized for balancing.
- **Pitta (Fire/Water)**: Cooling, moderately heavy, and slightly dry foods are prioritized.
- **Kapha (Earth/Water)**: Light, warming, and stimulating/drying foods are prioritized.

### Triple-Attribute Food Profile
Each food in our database is profiled using the traditional Ayurvedic framework:
1.  **Rasa (Taste)**: Sweet, Sour, Salty, Pungent, Bitter, Astringent.
2.  **Virya (Potency)**: Specifically focused on **Heating (Ushna)** or **Cooling (Sheeta)** effects.
3.  **Vipaka (Post-Digestive Effect)**: The long-term impact on the tissues (Sweet, Sour, or Pungent).

### Selection Strategy
- **Opposite Qualities (Samanya Vishesha)**: If a patient has a "High Pitta" (Heat) imbalance, the engine prioritizes foods with "Sheeta Virya" (Cooling Potency) and "Sweet/Bitter Rasa".
- **Vikriti Score**: Foods with a negative score for a specific Dosha (e.g., Vata Effect = -1) are "Vata-Pacifying" and are weighted higher during generation.

---

## 3. Conflict Detection & Safety Protocol

The safety layer (Apathya) ensures that nutritional advice does not conflict with existing medical conditions.

### Apathya Cross-Referencing
The system maintains a matrix of **Medical Conditions vs. Food Contraindications**:
- **Example**: A patient with "Acidity" (Amila-pitta) will have foods with "Sour Rasa" and "Heating Virya" automatically flagged as conflicts, regardless of their other nutritional benefits.
- **Conflict Badges**: Every meal card in the system provides a visual bridge explaining *why* a food was selected or why it might be a risk.

---

## 4. Weekly Generation Logic

To prevent "monotony of diet" and ensure a broad micro-nutrient profile, the 7-day generator implements:

- **Slot Prioritization**: Templates define specific category priorities (e.g., Grains for breakfast, Vegetables for dinner).
- **Randomized Candidate Selection**: The engine identifies a pool of "Clinical Best Fits" and uses a randomization algorithm to ensure variety across the 7-day plan.
- **Periodic Checks**: The system recalculates total weekly averages to ensure the randomized choices still meet the patient's long-term target within a 5% margin of error.

---

## 5. Summary of Clinical Workflow
1.  **Vitals Intake**: Patient parameters are collected.
2.  **Dosha Assessment**: Practitioner determines Vikriti via the integrated scoring system.
3.  **Target Baselining**: BMR and TDEE are established.
4.  **Template Selection**: Practitioner selects a therapeutic goal (e.g., Weight Loss, Balancing).
5.  **Multi-Day Generation**: Randomization engine populates 7 days of Pathya meals.
6.  **Interactive Review**: Practitioner fine-tunes portions, observing real-time macro updates.

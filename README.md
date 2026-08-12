# 🌿 AyurDiet Pro

> **Clinical-Grade Ayurvedic Nutrition & Diet Planning Platform**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://ayurdietpro-up4f.onrender.com)
[![React](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**AyurDiet Pro** is a clinical decision-support tool for Ayurvedic practitioners. It bridges classical Ayurvedic wisdom — Prakriti assessment, Dosha balancing, Rasa/Virya/Vipaka logic — with modern nutritional science including BMR calculation and macro-nutrient targeting.

🔗 **Live:** https://ayurdietpro-up4f.onrender.com

---

## 📋 Table of Contents

- [Key Features](#-key-features)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [Architecture](#️-architecture)
- [Getting Started](#-getting-started)
- [API Overview](#-api-overview)
- [Clinical Methodology](#-clinical-methodology)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Key Features

- **Clinical Intake Form** — Comprehensive sectioned patient form covering vitals, digestive history, and behavioral data.
- **Ayur-Logic Engine** — Automatically calculates Prakriti/Vikriti and recommends foods based on Virya, Rasa, Vipaka, and Dosha-specific impacts.
- **Interactive Diet Builder:**
  - 7-day weekly meal schedule planning
  - Real-time macro gauges vs. calculated clinical targets (BMR/TDEE)
  - Intelligent randomized plan generation from clinical templates
- **Apathya (Contraindication) Check** — Cross-references medical conditions (Acidity, IBS, Diabetes, etc.) with food contraindications and surfaces clinical alerts with logical reasoning.
- **Weekly Insights Dashboard** — Practitioner activity, patient trends, and Vikriti distribution over a rolling 7-day window.
- **PDF Export** — Patient-facing diet charts ready for distribution, generated with jsPDF + AutoTable.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js, Vite, Vanilla CSS (Glassmorphism) |
| **Backend** | FastAPI (Python), SQLAlchemy ORM |
| **Database** | SQLite |
| **Auth** | JWT-based Authentication |
| **PDF** | jsPDF, AutoTable |
| **Deployment** | Render |

---

## 📁 Project Structure

```
AyurDietPro/
├── client/                          # React + Vite frontend
│   ├── public/
│   ├── src/
│   │   ├── assets/                  # Static assets (icons, images)
│   │   ├── components/              # Reusable UI components
│   │   │   ├── MacroGauge.jsx       # Real-time macro tracking gauge
│   │   │   ├── MealCard.jsx         # Meal slot display card
│   │   │   ├── ConflictAlert.jsx    # Apathya clinical alert banner
│   │   │   └── PatientCard.jsx      # Patient summary widget
│   │   ├── pages/                   # Practitioner workflow pages
│   │   │   ├── PatientForm.jsx      # Clinical intake form
│   │   │   ├── DietBuilder.jsx      # 7-day diet plan builder
│   │   │   ├── Dashboard.jsx        # Weekly insights dashboard
│   │   │   └── Reports.jsx          # PDF export page
│   │   ├── services/                # Axios API call wrappers
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── server/                          # FastAPI Python backend
│   ├── engine/                      # Core Ayurvedic logic
│   │   ├── ayur_logic.py            # Food recommendation engine (Virya/Rasa/Vipaka)
│   │   └── conflict_checker.py      # Apathya contraindication detection
│   ├── routes/                      # Modular API endpoints
│   │   ├── auth.py                  # Register / login / JWT
│   │   ├── patients.py              # Patient CRUD & history
│   │   ├── diet.py                  # Diet plan generation & retrieval
│   │   ├── foods.py                 # Food database queries
│   │   └── reports.py               # PDF chart generation
│   ├── models/                      # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── food.py
│   │   └── diet_plan.py
│   ├── database.py                  # DB connection, init & seed
│   ├── requirements.txt
│   └── main.py                      # FastAPI entry point
│
├── METHODOLOGY.md                   # Full clinical methodology documentation
├── README.md
├── start-production.bat             # Windows: build frontend + serve from FastAPI
└── start-production.sh              # macOS/Linux: build frontend + serve from FastAPI
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              Patient Intake & Vitals                │
│       (Prakriti • Vikriti • Medical History)        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│               Ayur-Logic Engine                     │
│  Dosha Balancing │ Virya/Rasa/Vipaka │ Apathya      │
│  BMR/TDEE Calc   │ Macro Targets     │ Conflict Flag │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│          Personalized 7-Day Diet Chart              │
│      (PDF Export • Macro Tracking • Variety)        │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+

### Backend Setup

```bash
cd server
pip install -r requirements.txt
python main.py
```

> The database initializes and seeds with default foods and templates on first run.

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`, API at `http://localhost:8000`.

### Production (Single Service — No Docker)

Compiles the frontend and serves everything from the FastAPI server on port `8000`.

**Windows:**
```cmd
start-production.bat
```

**macOS / Linux:**
```bash
chmod +x start-production.sh
./start-production.sh
```

---

## 🔌 API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register` | Register a new practitioner |
| `POST` | `/api/auth/login` | Authenticate & receive JWT |
| `POST` | `/api/patients` | Create patient record with intake data |
| `GET` | `/api/patients/:id` | Fetch patient profile & history |
| `POST` | `/api/diet/generate` | Generate 7-day diet plan from Prakriti |
| `GET` | `/api/foods?dosha=pitta` | Query foods by Dosha compatibility |
| `POST` | `/api/reports/pdf` | Export diet chart as PDF |

Full spec: [`METHODOLOGY.md`](METHODOLOGY.md)

---

## 🧪 Clinical Methodology

See [`METHODOLOGY.md`](METHODOLOGY.md) for the full breakdown. Summary:

**1. Nutritional Foundation**
BMR via the Mifflin-St Jeor Equation, activity-adjusted (multipliers 1.2–1.9), with a standard macro split of 55% Carbs / 20% Protein / 25% Fat.

**2. Ayur-Logic Engine**
Three-tier food compatibility check: Vikriti balancing → Virya alignment → Rasa/Vipaka attribute matching for holistic Pathya recommendations.

**3. Safety Layer**
Apathya Check flags Dosha-food conflicts and medical contraindications with visual alerts and practitioner-readable reasoning.

**4. Scheduling**
7-day horizon with meal-slot-specific category prioritization and intelligent randomization for variety and adherence.

---

## 🗺️ Roadmap

- [ ] Ritucharya (Seasonal) integration with climate-based auto-adjustments
- [ ] Smart ingredient swapping while preserving Virya/Rasa profiles
- [ ] Patient portal with meal tracking and digestive feedback
- [ ] Grocery list automation grouped by market section
- [ ] Longitudinal Vikriti trend analytics across consultations
- [ ] Dina Charya (Ayurvedic clock) aware macro scheduling

---

## 🤝 Contributing

1. Fork the project
2. Create your branch: `git checkout -b feature/AyurFeature`
3. Commit: `git commit -m 'Add AyurFeature'`
4. Push: `git push origin feature/AyurFeature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## 📧 Contact

**Kunal Soyane** — [github.com/KunalSoyane](https://github.com/KunalSoyane)

Project: https://github.com/KunalSoyane/AyurDietPro | Demo: https://ayurdietpro-up4f.onrender.com

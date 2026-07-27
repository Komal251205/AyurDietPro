import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function DashboardPage() {
  const [patients, setPatients] = useState([]);
  const [plans, setPlans] = useState([]);

  useEffect(() => {
    api.patients().then(setPatients).catch(() => setPatients([]));
    api.dietPlans().then(setPlans).catch(() => setPlans([]));
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <div className="grid3">
        <div className="card">Total Patients: {patients.length}</div>
        <div className="card">Charts Generated: {plans.length}</div>
        <div className="card">Foods in DB: Seeded</div>
      </div>
      <div className="card">
        <h3>Quick Actions</h3>
        <div className="row">
          <Link to="/patients/new" className="primary-btn">
            New Patient
          </Link>
          <Link to="/foods" className="ghost-btn">
            Food Explorer
          </Link>
        </div>
      </div>
    </div>
  );
}


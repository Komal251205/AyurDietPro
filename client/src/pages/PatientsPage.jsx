import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function PatientsPage() {
  const [patients, setPatients] = useState([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    api.patients().then(setPatients);
  }, []);

  const filtered = patients.filter((p) => p.name.toLowerCase().includes(query.toLowerCase()));

  return (
    <div>
      <div className="row spread">
        <h2>Patients</h2>
        <Link to="/patients/new" className="primary-btn">
          Add Patient
        </Link>
      </div>
      <input placeholder="Search patient" value={query} onChange={(e) => setQuery(e.target.value)} />
      <div className="card">
        {filtered.map((patient) => (
          <div key={patient.id} className="row spread line">
            <span>
              {patient.name} | {patient.vikriti}
            </span>
            <span>
              <Link to={`/patients/${patient.id}`}>View</Link> |{" "}
              <Link to={`/patients/${patient.id}/edit`}>Edit</Link> |{" "}
              <Link to={`/patients/${patient.id}/diet`}>Create Diet</Link> |{" "}
              <button
                className="text-btn danger"
                onClick={async () => {
                  if (window.confirm("Are you sure you want to delete this patient?")) {
                    await api.deletePatient(patient.id);
                    setPatients(patients.filter((p) => p.id !== patient.id));
                  }
                }}
              >
                Delete
              </button>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}


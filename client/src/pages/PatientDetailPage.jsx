import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";

export default function PatientDetailPage() {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);

  useEffect(() => {
    api.patient(id).then(setPatient);
  }, [id]);

  if (!patient) return <div>Loading...</div>;

  return (
    <div className="card">
      <h2>{patient.name}</h2>
      <p>
        {patient.age} yrs | {patient.gender} | Vikriti: {patient.vikriti}
      </p>
      <p>Conditions: {(patient.conditions || []).join(", ") || "None"}</p>
      <Link className="primary-btn" to={`/patients/${id}/diet`}>
        Generate Diet Plan
      </Link>
    </div>
  );
}


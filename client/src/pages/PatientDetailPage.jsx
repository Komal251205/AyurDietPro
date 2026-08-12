import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";

export default function PatientDetailPage() {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);

  useEffect(() => {
    if (id && id !== "undefined") {
      api.patient(id).then(setPatient).catch(console.error);
    }
  }, [id]);

  if (!patient) return <div className="card">Loading...</div>;

  const patientId = patient._id || patient.id || id;

  return (
    <div className="card">
      <h2>{patient.name}</h2>
      <p>
        {patient.age} yrs | {patient.gender} | Vikriti: {patient.vikriti}
      </p>
      <p>Conditions: {(patient.conditions || []).join(", ") || "None"}</p>
      <Link className="primary-btn" to={`/patients/${patientId}/diet`}>
        Generate Diet Plan
      </Link>
    </div>
  );
}
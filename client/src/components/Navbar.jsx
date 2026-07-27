import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="navbar">
      <div className="brand">AyurDiet Pro</div>
      <nav>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/patients">Patients</Link>
        <Link to="/reports">Weekly Report</Link>
        <Link to="/foods">Food Explorer</Link>
      </nav>
      <button
        className="ghost-btn"
        onClick={() => {
          logout();
          navigate("/login");
        }}
      >
        Logout
      </button>
    </header>
  );
}


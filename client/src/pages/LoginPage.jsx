import { useState } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("doctor@ayurdiet.com");
  const [password, setPassword] = useState("demo1234");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      if (err.status === 401) {
        setError("Invalid email or password.");
      } else {
        setError(err.message || "Unable to login right now.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <form className="card auth-card" onSubmit={handleSubmit}>
        <h1>AyurDiet Pro</h1>
        <p className="muted">Clinical Ayurvedic diet planning</p>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        {error && <p className="error">{error}</p>}
        <button className="primary-btn" type="submit" disabled={submitting}>
          {submitting ? "Signing in..." : "Login"}
        </button>
        <p className="muted">
          New doctor? <Link to="/register">Create account</Link>
        </p>
      </form>
    </div>
  );
}


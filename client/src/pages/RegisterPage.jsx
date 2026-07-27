import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function passwordStrength(password) {
  let score = 0;
  if (password.length >= 8) score += 1;
  if (/[A-Z]/.test(password)) score += 1;
  if (/[a-z]/.test(password)) score += 1;
  if (/\d/.test(password)) score += 1;
  if (/[^A-Za-z0-9]/.test(password)) score += 1;

  if (score <= 2) return { label: "Weak", className: "weak", value: 33 };
  if (score <= 4) return { label: "Medium", className: "medium", value: 66 };
  return { label: "Strong", className: "strong", value: 100 };
}

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();
  const emailValid = emailRegex.test(email.trim());
  const strength = passwordStrength(password);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!emailValid) {
      setError("Please enter a valid email address.");
      return;
    }
    if (strength.label === "Weak") {
      setError("Password is too weak. Use 8+ chars with uppercase, number, and symbol.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setSubmitting(true);
    try {
      await api.register({ name, email, password });
      setSuccess("Registration successful. Please login.");
      setTimeout(() => navigate("/login"), 800);
    } catch (err) {
      if (err.status === 409) {
        setError("Email is already registered. Try logging in.");
      } else {
        setError(err.message || "Unable to register right now.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <form className="card auth-card" onSubmit={handleSubmit}>
        <h1>Create Account</h1>
        <p className="muted">Register doctor access for AyurDiet Pro</p>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Full Name" required />
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
        {email && !emailValid && <p className="error">Enter a valid email format (e.g., doctor@clinic.com).</p>}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password (min 6 chars)"
          required
          minLength={6}
        />
        <div className="strength-wrap">
          <div className="strength-bar">
            <div className={`strength-fill ${strength.className}`} style={{ width: `${strength.value}%` }} />
          </div>
          <p className="muted">
            Password Strength: <span className={`strength-text ${strength.className}`}>{strength.label}</span>
          </p>
        </div>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
          required
        />
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
        <button className="primary-btn" type="submit" disabled={submitting}>
          {submitting ? "Creating..." : "Register"}
        </button>
        <p className="muted">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}


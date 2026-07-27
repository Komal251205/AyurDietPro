import { createContext, useContext, useMemo, useState } from "react";
import { Navigate } from "react-router-dom";
import { api } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const value = useMemo(
    () => ({
      token,
      isAuthenticated: Boolean(token),
      async login(email, password) {
        const data = await api.login(email, password);
        localStorage.setItem("token", data.access_token);
        setToken(data.access_token);
      },
      logout() {
        localStorage.removeItem("token");
        setToken(null);
      },
    }),
    [token]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}

export function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
}


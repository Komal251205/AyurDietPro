import { Navigate, Route, Routes } from "react-router-dom";
import GlobalErrorBanner from "./components/GlobalErrorBanner";
import { ProtectedRoute } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import DashboardPage from "./pages/DashboardPage";
import DietChartPage from "./pages/DietChartPage";
import FoodExplorerPage from "./pages/FoodExplorerPage";
import LoginPage from "./pages/LoginPage";
import PatientDetailPage from "./pages/PatientDetailPage";
import PatientFormPage from "./pages/PatientFormPage";
import PatientViewPage from "./pages/PatientViewPage";
import PatientsPage from "./pages/PatientsPage";
import RegisterPage from "./pages/RegisterPage";
import WeeklyReportPage from "./pages/WeeklyReportPage";

function ProtectedLayout({ children }) {
  return (
    <>
      <Navbar />
      <main className="container">{children}</main>
    </>
  );
}

export default function App() {
  return (
    <>
      <GlobalErrorBanner />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <ProtectedLayout>
                <DashboardPage />
              </ProtectedLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/patients"
          element={
            <ProtectedRoute>
              <ProtectedLayout>
                <PatientsPage />
              </ProtectedLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/patients/new"
          element={
            <ProtectedRoute>
              <ProtectedLayout>
                <PatientFormPage />
              </ProtectedLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/patients/:id/edit"
          element={
            <ProtectedRoute>
              <ProtectedLayout>
                <PatientFormPage />
              </ProtectedLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/patients/:id"
          element={
            <ProtectedRoute>
              <ProtectedLayout>
                <PatientDetailPage />
              </ProtectedLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/patients/:id/diet"
          element={
            <ProtectedRoute>
              <ProtectedLayout>
                <DietChartPage />
              </ProtectedLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/foods"
          element={
            <ProtectedRoute>
              <ProtectedLayout>
                <FoodExplorerPage />
              </ProtectedLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/reports"
          element={
            <ProtectedRoute>
              <ProtectedLayout>
                <WeeklyReportPage />
              </ProtectedLayout>
            </ProtectedRoute>
          }
        />
        <Route path="/plan/:id/view" element={<PatientViewPage />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </>
  );
}


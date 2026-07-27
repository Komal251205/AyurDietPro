const BASE_URL = import.meta.env.VITE_API_URL || "/api";

async function request(path, options = {}) {
  const token = localStorage.getItem("token");
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    let message = "Request failed";
    if (Array.isArray(data.detail) && data.detail[0]?.msg) {
      message = data.detail[0].msg;
    } else if (typeof data.detail === "string") {
      message = data.detail;
    } else if (data.message) {
      message = data.message;
    } else if (!navigator.onLine) {
      message = "No internet connection.";
    }
    const error = new Error(message);
    error.status = response.status;
    if (!options.suppressGlobalError) {
      window.dispatchEvent(
        new CustomEvent("api-error", {
          detail: { message, status: response.status },
        })
      );
    }
    throw error;
  }
  return response.json();
}

export const api = {
  login: (email, password) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      suppressGlobalError: true,
    }),
  register: (payload) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
      suppressGlobalError: true,
    }),
  patients: () => request("/patients"),
  createPatient: (payload) => request("/patients", { method: "POST", body: JSON.stringify(payload) }),
  patient: (id) => request(`/patients/${id}`),
  updatePatient: (id, payload) => request(`/patients/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deletePatient: (id) => request(`/patients/${id}`, { method: "DELETE" }),
  templates: () => request("/templates"),
  generatePlan: (payload) => request("/diet-plans/generate", { method: "POST", body: JSON.stringify(payload) }),
  dietPlans: () => request("/diet-plans"),
  getPlan: (id) => request(`/diet-plans/${id}`),
  patientPlans: (patientId) => request(`/diet-plans/patient/${patientId}`),
  updatePlan: (id, payload) => request(`/diet-plans/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  foods: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/foods${q ? `?${q}` : ""}`);
  },
  foodCategories: () => request("/foods/categories"),
  getWeeklyReport: () => request("/reports/weekly"),
};


const BASE_URL = import.meta.env.VITE_API_URL || "/api";

async function request(path, options = {}) {
  // Destructure custom parameters out of options before passing options to fetch
  const { suppressGlobalError, ...fetchOptions } = options;

  const token = localStorage.getItem("token");
  const headers = {
    "Content-Type": "application/json",
    ...(fetchOptions.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    let message = "Request failed";

    // Extract detailed FastAPI validation errors
    if (Array.isArray(data.detail) && data.detail[0]?.msg) {
      const field = data.detail[0].loc?.[1] ? `[${data.detail[0].loc[1]}]: ` : "";
      message = `${field}${data.detail[0].msg}`;
    } else if (typeof data.detail === "string") {
      message = data.detail;
    } else if (data.message) {
      message = data.message;
    } else if (!navigator.onLine) {
      message = "No internet connection.";
    }

    const error = new Error(message);
    error.status = response.status;

    if (!suppressGlobalError) {
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
  // Auth
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

  // Patients
  patients: () => request("/patients"),
  createPatient: (payload) =>
    request("/patients", { method: "POST", body: JSON.stringify(payload) }),
  patient: (id) => request(`/patients/${id}`),
  updatePatient: (id, payload) =>
    request(`/patients/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deletePatient: (id) => request(`/patients/${id}`, { method: "DELETE" }),

  // Foods & Templates
  foods: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/foods${q ? `?${q}` : ""}`);
  },
  foodCategories: () => request("/foods/categories"),
  templates: () => request("/templates"),

  // Diet Plans
  generatePlan: (payload) =>
    request("/diet-plans/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  dietPlans: () => request("/diet-plans"),
  getPlan: (id) => request(`/diet-plans/${id}`),
  patientPlans: (patientId) => request(`/diet-plans/patient/${patientId}`),
  updatePlan: (id, payload) =>
    request(`/diet-plans/${id}`, { method: "PUT", body: JSON.stringify(payload) }),

  // Reports
  getWeeklyReport: () => request("/reports/weekly"),
};
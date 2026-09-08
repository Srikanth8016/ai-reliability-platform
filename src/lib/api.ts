export const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export function getAuthToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("auth_token");
  }
  return null;
}

export function setAuthToken(token: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem("auth_token", token);
  }
}

export function clearAuthToken() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("auth_token");
  }
}

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const token = getAuthToken();
  const headers = new Headers(options.headers || {});
  
  headers.set("Content-Type", "application/json");
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const config: RequestInit = {
    ...options,
    headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || `API Error: ${response.status}`);
  }

  return response.json();
}

const API_BASE_URL = "http://127.0.0.1:5000";

async function apiRequest(endpoint, options = {}) {
  const config = {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  let data = {};
  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.error || "Request failed.");
  }

  return data;
}

export async function signup(payload) {
  return apiRequest("/signup", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function login(payload) {
  return apiRequest("/login", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function logout() {
  return apiRequest("/logout", {
    method: "POST"
  });
}

export async function getCurrentUser() {
  return apiRequest("/me", {
    method: "GET"
  });
}

export async function getProfile() {
  return apiRequest("/profile", {
    method: "GET"
  });
}

export async function updateProfile(payload) {
  return apiRequest("/profile", {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export async function getProfiles(params = {}) {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== "" && value !== null && value !== undefined) {
      searchParams.append(key, value);
    }
  });

  const queryString = searchParams.toString();
  const endpoint = queryString ? `/profiles?${queryString}` : "/profiles";

  return apiRequest(endpoint, {
    method: "GET"
  });
}
import { CSRF_TOKEN } from "./csrf_token.js";

async function getJSON(response) {
  if (response.status === 204) return "";
  return response.json();
}

function apiService(endpoint, method, data) {
  const config = {
    method: method || "GET",
    body: data !== undefined ? JSON.stringify(data) : null,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": CSRF_TOKEN
    }
  };
  return fetch(endpoint, config)
    .then(getJSON)
    .catch(error => alert(error));
}

function apiService_formData(endpoint, method, data) {
  const config = {
    method: method || "GET",
    body: data !== undefined ? data : null,
    headers: {
      "X-CSRFTOKEN": CSRF_TOKEN
    }
  };
  return fetch(endpoint, config)
    .then(getJSON)
    .catch(error => alert(error));
}

export { apiService, apiService_formData };
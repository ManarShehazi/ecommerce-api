/**
 * Centralized API client using axios.
 *
 * - Base URL points to the FastAPI backend
 * - Auth token is attached automatically to every request via interceptor
 * - Token is stored in localStorage so it survives page refreshes
 */

import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach the session token to every outgoing request (if logged in)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Auth ──────────────────────────────────────────────

export async function register(username, password) {
  const { data } = await api.post("/auth/register", { username, password });
  return data;
}

export async function login(username, password) {
  const { data } = await api.post("/auth/login", { username, password });
  return data;
}

// ── Products ──────────────────────────────────────────

export async function fetchProducts() {
  const { data } = await api.get("/products/");
  return data;
}

// ── Credits ───────────────────────────────────────────

export async function addCredits() {
  const { data } = await api.post("/credits/add");
  return data;
}

export async function getBalance() {
  const { data } = await api.get("/credits/");
  return data;
}

// ── Orders ────────────────────────────────────────────

export async function purchaseProduct(productId) {
  const { data } = await api.post("/orders/", { product_id: productId });
  return data;
}

export async function fetchOrders() {
  const { data } = await api.get("/orders/");
  return data;
}

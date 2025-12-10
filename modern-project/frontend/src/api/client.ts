import axios from "axios";
import { useSessionStore } from "../stores/session";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const session = useSessionStore();
  if (session.token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${session.token}`;
  }
  return config;
});

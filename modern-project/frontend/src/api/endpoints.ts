import { api } from "./client";

export async function login(username: string, password: string) {
  const { data } = await api.post("/auth/token", { username, password });
  return data as { access_token: string; token_type: string };
}

export async function fetchProfile() {
  const { data } = await api.get("/auth/me");
  return data as { username: string; roles: string[] };
}

export async function listTenants() {
  const { data } = await api.get("/tenants/");
  return data;
}

export async function createTenant(payload: any) {
  const { data } = await api.post("/tenants/", payload);
  return data;
}

export async function fetchUsers(tenantId: number) {
  const { data } = await api.get(`/users/${tenantId}`);
  return data;
}

export async function fetchLicenses(tenantId: number) {
  const { data } = await api.get(`/licenses/${tenantId}`);
  return data;
}

export async function fetchInvites(tenantId: number) {
  const { data } = await api.get(`/invites/${tenantId}`);
  return data;
}

export async function fetchReports(tenantId: number) {
  const { data } = await api.get(`/reports/${tenantId}`);
  return data;
}

export async function updateSetting(key: string, value: string) {
  const { data } = await api.put(`/settings/${key}`, { key, value });
  return data;
}

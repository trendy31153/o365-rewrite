import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { fetchProfile, login } from "../api/endpoints";

export const useSessionStore = defineStore("session", () => {
  const token = ref<string | null>(localStorage.getItem("token"));
  const username = ref<string | null>(localStorage.getItem("username"));
  const roles = ref<string[]>(JSON.parse(localStorage.getItem("roles") || "[]"));

  const isAuthenticated = computed(() => Boolean(token.value && username.value));

  async function signIn(user: string, password: string) {
    const response = await login(user, password);
    token.value = response.access_token;
    username.value = user;
    localStorage.setItem("token", token.value);
    localStorage.setItem("username", user);
    try {
      await loadProfile();
    } catch (error) {
      signOut();
      throw error;
    }
  }

  function signOut() {
    token.value = null;
    username.value = null;
    roles.value = [];
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("roles");
  }

  async function loadProfile() {
    if (!token.value) return;
    const profile = await fetchProfile();
    username.value = profile.username;
    roles.value = profile.roles;
    localStorage.setItem("roles", JSON.stringify(profile.roles));
  }

  return { token, username, roles, isAuthenticated, signIn, signOut, loadProfile };
});

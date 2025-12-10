import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { login } from "../api/endpoints";

export const useSessionStore = defineStore("session", () => {
  const token = ref<string | null>(null);
  const username = ref<string | null>(null);

  const isAuthenticated = computed(() => Boolean(token.value));

  async function signIn(user: string, password: string) {
    const response = await login(user, password);
    token.value = response.access_token;
    username.value = user;
  }

  function signOut() {
    token.value = null;
    username.value = null;
  }

  return { token, username, isAuthenticated, signIn, signOut };
});

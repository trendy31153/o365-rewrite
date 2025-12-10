<template>
  <AppShell>
    <template #actions>
      <el-button size="small" @click="signOut">Sign out</el-button>
    </template>
    <router-view />
  </AppShell>
</template>

<script setup lang="ts">
import AppShell from "../components/AppShell.vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "../stores/session";

const router = useRouter();
const session = useSessionStore();

function signOut() {
  session.signOut();
  router.push({ name: "login" });
}
</script>

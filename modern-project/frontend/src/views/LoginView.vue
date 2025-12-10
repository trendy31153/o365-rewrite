<template>
  <div class="login">
    <el-card class="card">
      <h2>O365 Admin Login</h2>
      <el-form @submit.prevent="submit" label-position="top">
        <el-form-item label="Username">
          <el-input v-model="username" autocomplete="username" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="password" type="password" autocomplete="current-password" />
        </el-form-item>
        <el-button type="primary" :loading="loading" @click="submit" block>Sign in</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "../stores/session";

const router = useRouter();
const session = useSessionStore();
const username = ref("admin");
const password = ref("admin");
const loading = ref(false);

async function submit() {
  loading.value = true;
  try {
    await session.signIn(username.value, password.value);
    router.push("/");
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(circle at 20% 20%, rgba(56, 189, 248, 0.25), transparent 40%), #0f172a;
}

.card {
  width: 360px;
}
</style>

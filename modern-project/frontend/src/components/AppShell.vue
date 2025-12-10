<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">Modern O365</div>
      <el-menu :default-active="active" router background-color="#0b1224" text-color="#cbd5e1" active-text-color="#38bdf8">
        <el-menu-item index="/tenants">Tenants</el-menu-item>
        <el-menu-item index="/users">Users</el-menu-item>
        <el-menu-item index="/licenses">Licenses</el-menu-item>
        <el-menu-item index="/invites">Invites</el-menu-item>
        <el-menu-item index="/reports">Reports</el-menu-item>
        <el-menu-item index="/settings">Settings</el-menu-item>
      </el-menu>
    </aside>
    <main class="content">
      <header class="header">
        <slot name="actions" />
      </header>
      <section class="body">
        <slot />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const active = computed(() => route.path);
</script>

<style scoped>
.shell {
  display: grid;
  grid-template-columns: 240px 1fr;
  height: 100vh;
}

.sidebar {
  background: #0b1224;
  border-right: 1px solid #1f2937;
  color: #cbd5e1;
}

.brand {
  padding: 16px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #38bdf8;
}

.content {
  display: flex;
  flex-direction: column;
  background: radial-gradient(circle at 20% 20%, rgba(56, 189, 248, 0.15), transparent 35%),
    radial-gradient(circle at 80% 0%, rgba(94, 234, 212, 0.12), transparent 30%),
    #0f172a;
}

.header {
  display: flex;
  justify-content: flex-end;
  padding: 12px 24px;
  border-bottom: 1px solid #1f2937;
}

.body {
  padding: 24px;
  overflow-y: auto;
}
</style>

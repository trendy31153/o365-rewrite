<template>
  <main class="p-6 font-sans text-slate-900">
    <header class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Modern O365 Admin Panel</h1>
        <p class="text-sm text-slate-600">FastAPI + Vue 3 rewrite of the legacy management console</p>
      </div>
      <button class="rounded bg-indigo-600 px-4 py-2 text-white" @click="refresh">Refresh Data</button>
    </header>
    <DashboardView />
  </main>
</template>

<script setup lang="ts">
import DashboardView from './views/DashboardView.vue'
import { useTenantStore } from './stores/tenant'

const tenant = useTenantStore()

const refresh = () => {
  tenant.fetchOrganization()
  tenant.fetchSystemStatus()
}
</script>

<style scoped>
main {
  max-width: 1200px;
  margin: 0 auto;
}
button {
  transition: transform 0.1s ease-in-out;
}
button:hover {
  transform: translateY(-1px);
}
</style>

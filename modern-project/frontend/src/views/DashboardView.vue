<template>
  <div class="space-y-6">
    <div class="grid gap-4 md:grid-cols-2">
      <UserTable />
      <InviteDrawer />
    </div>

    <section class="rounded border border-slate-200 p-4">
      <header class="mb-3 flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold">Tenant</h2>
          <p class="text-xs text-slate-600">Domains, organization metadata, and feature toggles.</p>
        </div>
        <button class="rounded border px-3 py-1 text-sm" @click="refresh">Reload</button>
      </header>

      <div v-if="tenant.organization" class="mb-2 text-sm">
        <p class="font-medium">{{ tenant.organization.display_name }}</p>
        <p class="text-slate-600">Tenant ID: {{ tenant.organization.tenant_id }}</p>
      </div>

      <div class="mb-4">
        <h3 class="text-xs uppercase text-slate-500">Domains</h3>
        <ul class="list-disc pl-5 text-sm">
          <li v-for="domain in tenant.organization?.domains" :key="domain.id">
            {{ domain.name }}<span v-if="domain.default" class="ml-2 text-xs text-emerald-600">(default)</span>
          </li>
        </ul>
      </div>

      <div class="flex gap-4 text-sm">
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="multiTenant" /> Multi-tenant
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="inviteOnly" /> Invite only
        </label>
        <label class="flex items-center gap-2">
          <input type="checkbox" v-model="selfService" /> Allow self-service signup
        </label>
        <button class="rounded bg-indigo-600 px-3 py-1 text-white" @click="save">Save</button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import InviteDrawer from '../components/InviteDrawer.vue'
import UserTable from '../components/UserTable.vue'
import { useTenantStore } from '../stores/tenant'

const tenant = useTenantStore()
const multiTenant = ref(false)
const inviteOnly = ref(false)
const selfService = ref(true)

const refresh = async () => {
  await tenant.fetchOrganization()
  await tenant.fetchSystemStatus()
  multiTenant.value = tenant.systemStatus?.multi_tenant_enabled ?? false
  inviteOnly.value = tenant.systemStatus?.invite_only_mode ?? false
  selfService.value = tenant.systemStatus?.allow_user_registration ?? true
}

const save = async () => {
  await tenant.updateSystemStatus({
    multi_tenant_enabled: multiTenant.value,
    invite_only_mode: inviteOnly.value,
    allow_user_registration: selfService.value,
  })
}

onMounted(refresh)
</script>

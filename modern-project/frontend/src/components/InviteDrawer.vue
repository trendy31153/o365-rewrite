<template>
  <section class="rounded border border-slate-200 p-4">
    <header class="mb-3">
      <h2 class="text-lg font-semibold">Invitations</h2>
      <p class="text-xs text-slate-600">Generate invitation links for multi-tenant onboarding.</p>
    </header>

    <div class="mb-3 flex gap-2">
      <input v-model="email" placeholder="user@domain.com" class="flex-1 rounded border px-2 py-1 text-sm" />
      <input v-model="role" placeholder="Role (optional)" class="rounded border px-2 py-1 text-sm" />
      <button class="rounded bg-indigo-500 px-3 py-1 text-white" @click="create">Create invite</button>
    </div>

    <div class="space-y-2">
      <div
        v-for="invite in invites"
        :key="invite.id"
        class="flex items-center justify-between rounded border px-3 py-2 text-sm"
      >
        <div>
          <p class="font-medium">{{ invite.email }}</p>
          <p class="text-xs text-slate-500">Expires: {{ format(invite.expires_at) }}</p>
        </div>
        <a class="text-indigo-600" :href="invite.redeem_url" target="_blank">Redeem</a>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../stores/api'

type Invite = {
  id: string
  email: string
  redeem_url: string
  created_at: string
  expires_at: string | null
  role?: string | null
}

const invites = ref<Invite[]>([])
const email = ref('')
const role = ref('')

const load = async () => {
  const { data } = await api.get<Invite[]>('/invites')
  invites.value = data
}

const create = async () => {
  const { data } = await api.post<Invite>('/invites', null, { params: { email: email.value, role: role.value || undefined } })
  invites.value.unshift(data)
  email.value = ''
  role.value = ''
}

const format = (value: string | null) => (value ? new Date(value).toLocaleString() : 'No expiry')

onMounted(load)
</script>

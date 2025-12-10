<template>
  <section class="rounded border border-slate-200 p-4">
    <header class="mb-3 flex items-center justify-between">
      <div>
        <h2 class="text-lg font-semibold">Users</h2>
        <p class="text-xs text-slate-600">Create, search, and license users.</p>
      </div>
      <div class="flex gap-2">
        <input v-model="keyword" placeholder="Search UPN" class="rounded border px-2 py-1 text-sm" />
        <button class="rounded bg-slate-800 px-3 py-1 text-white" @click="search">Search</button>
      </div>
    </header>

    <div class="grid grid-cols-6 gap-2 border-b pb-2 text-xs font-semibold uppercase text-slate-500">
      <span>Display name</span>
      <span>UPN</span>
      <span>Roles</span>
      <span>Licenses</span>
      <span>Status</span>
      <span></span>
    </div>

    <div v-for="user in store.list" :key="user.id" class="grid grid-cols-6 items-center gap-2 border-b py-2 text-sm">
      <span class="font-medium">{{ user.display_name }}</span>
      <span class="text-slate-600">{{ user.user_principal_name }}</span>
      <span>{{ user.roles.join(', ') }}</span>
      <span>{{ user.license_skus.join(', ') || 'None' }}</span>
      <span :class="user.status === 'active' ? 'text-emerald-600' : 'text-amber-600'">{{ user.status }}</span>
      <button class="rounded border border-indigo-500 px-2 py-1 text-xs text-indigo-600" @click="openLicenses(user)">
        Assign license
      </button>
    </div>

    <footer class="mt-4 flex gap-2">
      <input v-model="newUser.user_principal_name" placeholder="user@domain.com" class="flex-1 rounded border px-2 py-1 text-sm" />
      <input v-model="newUser.display_name" placeholder="Display name" class="flex-1 rounded border px-2 py-1 text-sm" />
      <input v-model="newUser.password" type="password" placeholder="Password" class="flex-1 rounded border px-2 py-1 text-sm" />
      <button class="rounded bg-indigo-600 px-4 py-2 text-white" @click="create">Create user</button>
    </footer>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useUserStore, type CreateUserRequest, type User } from '../stores/users'

const store = useUserStore()
const keyword = ref('')
const newUser = reactive<CreateUserRequest>({
  user_principal_name: '',
  display_name: '',
  password: '',
  license_skus: [],
})

const search = async () => {
  await store.fetchAll(keyword.value || undefined)
}

const create = async () => {
  await store.createUser({ ...newUser })
  Object.assign(newUser, { user_principal_name: '', display_name: '', password: '', license_skus: [] })
}

const openLicenses = (user: User) => {
  const sku = prompt('Enter SKU to assign', 'O365_E5')
  if (!sku) return
  store.assignLicenses(user.id, [sku])
}

onMounted(() => store.fetchAll())
</script>

<style scoped>
input:focus {
  outline: 1px solid #4f46e5;
}
</style>

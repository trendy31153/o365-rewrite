import { defineStore } from 'pinia'
import { api } from './api'

export type User = {
  id: string
  user_principal_name: string
  display_name: string
  roles: string[]
  license_skus: string[]
  invited: boolean
  status: 'active' | 'disabled' | 'pending'
}

export type CreateUserRequest = {
  user_principal_name: string
  display_name: string
  password: string
  force_change_password_next_sign_in?: boolean
  license_skus?: string[]
  usage_location?: string
}

export const useUserStore = defineStore('users', {
  state: () => ({
    list: [] as User[],
    roles: [] as string[],
    loading: false,
  }),
  actions: {
    async fetchAll(keyword?: string) {
      this.loading = true
      const { data } = await api.get<User[]>('/users', { params: { keyword } })
      this.list = data
      this.loading = false
    },
    async createUser(payload: CreateUserRequest) {
      const { data } = await api.post<User>('/users', payload)
      this.list.push(data)
    },
    async assignLicenses(userId: string, skuIds: string[]) {
      const { data } = await api.post<string[]>(`/users/${userId}/licenses`, skuIds)
      const target = this.list.find((u) => u.id === userId)
      if (target) target.license_skus = data
    },
    async fetchRoles() {
      const { data } = await api.get<string[]>('/users/roles')
      this.roles = data
    },
  },
})

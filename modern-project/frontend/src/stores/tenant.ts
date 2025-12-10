import { defineStore } from 'pinia'
import { api } from './api'

export type Domain = { id: string; name: string; verified: boolean; default: boolean }
export type Organization = { id: string; display_name: string; tenant_id: string; domains: Domain[] }
export type SystemStatus = { multi_tenant_enabled: boolean; invite_only_mode: boolean; allow_user_registration: boolean }

export const useTenantStore = defineStore('tenant', {
  state: () => ({
    organization: null as Organization | null,
    systemStatus: null as SystemStatus | null,
  }),
  actions: {
    async fetchOrganization() {
      const { data } = await api.get<Organization>('/domains/organization')
      this.organization = data
    },
    async fetchSystemStatus() {
      const { data } = await api.get<SystemStatus>('/system/status')
      this.systemStatus = data
    },
    async updateSystemStatus(payload: SystemStatus) {
      const { data } = await api.put<SystemStatus>('/system/status', payload)
      this.systemStatus = data
    },
  },
})

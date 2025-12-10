<template>
  <div>
    <div class="toolbar">
      <el-input v-model="tenantId" placeholder="Tenant record ID" style="max-width: 240px" />
      <el-button type="primary" @click="load">Load users</el-button>
    </div>
    <el-table :data="users" height="520">
      <el-table-column prop="display_name" label="Name" />
      <el-table-column prop="user_principal_name" label="UPN" />
      <el-table-column prop="enabled" label="Enabled">
        <template #default="{ row }">
          <el-tag :type="row.enabled ? 'success' : 'danger'">{{ row.enabled ? 'Enabled' : 'Disabled' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="roles" label="Roles" />
      <el-table-column prop="licenses" label="Licenses" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { fetchUsers } from "../api/endpoints";

const tenantId = ref<number | null>(null);
const users = ref<any[]>([]);

async function load() {
  if (!tenantId.value) return;
  users.value = await fetchUsers(tenantId.value);
}
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
</style>

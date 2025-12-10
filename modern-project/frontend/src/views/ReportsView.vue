<template>
  <div>
    <div class="toolbar">
      <el-input v-model="tenantId" placeholder="Tenant record ID" style="max-width: 240px" />
      <el-button type="primary" @click="load">Generate snapshot</el-button>
    </div>
    <el-table :data="reports" height="520">
      <el-table-column prop="generated_at" label="Generated" />
      <el-table-column prop="totals.users" label="Users" />
      <el-table-column prop="totals.admins" label="Admins" />
      <el-table-column prop="issues" label="Issues" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { fetchReports } from "../api/endpoints";

const tenantId = ref<number | null>(null);
const reports = ref<any[]>([]);

async function load() {
  if (!tenantId.value) return;
  reports.value = await fetchReports(tenantId.value);
}
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
</style>

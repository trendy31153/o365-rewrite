<template>
  <div>
    <div class="toolbar">
      <el-input v-model="tenantId" placeholder="Tenant record ID" style="max-width: 240px" />
      <el-button type="primary" @click="load">Load SKUs</el-button>
    </div>
    <el-table :data="licenses" height="520">
      <el-table-column prop="friendly_name" label="Product" />
      <el-table-column prop="sku_id" label="SKU" />
      <el-table-column prop="available" label="Available" />
      <el-table-column prop="assigned" label="Assigned" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { fetchLicenses } from "../api/endpoints";

const tenantId = ref<number | null>(null);
const licenses = ref<any[]>([]);

async function load() {
  if (!tenantId.value) return;
  licenses.value = await fetchLicenses(tenantId.value);
}
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
</style>

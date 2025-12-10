<template>
  <div>
    <div class="toolbar">
      <el-input v-model="tenantId" placeholder="Tenant record ID" style="max-width: 240px" />
      <el-button type="primary" @click="load">Load invites</el-button>
    </div>
    <el-table :data="invites" height="520">
      <el-table-column prop="code" label="Code" />
      <el-table-column prop="expires_at" label="Expires" />
      <el-table-column prop="used_count" label="Used" />
      <el-table-column prop="max_usage" label="Max" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { fetchInvites } from "../api/endpoints";

const tenantId = ref<number | null>(null);
const invites = ref<any[]>([]);

async function load() {
  if (!tenantId.value) return;
  invites.value = await fetchInvites(tenantId.value);
}
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
</style>

<template>
  <div class="grid">
    <el-card>
      <div class="card-header">
        <h3>Connected tenants</h3>
        <el-button type="primary" @click="load">Refresh</el-button>
      </div>
      <el-table :data="tenants" height="400">
        <el-table-column prop="display_name" label="Name" />
        <el-table-column prop="tenant_id" label="Tenant ID" />
        <el-table-column prop="client_id" label="Client ID" />
        <el-table-column label="Default">
          <template #default="{ row }">
            <el-tag type="success" v-if="row.is_default">Current</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-card>
      <div class="card-header">
        <h3>Add tenant</h3>
      </div>
      <el-form label-position="top">
        <el-form-item label="Display name">
          <el-input v-model="form.display_name" />
        </el-form-item>
        <el-form-item label="Tenant ID">
          <el-input v-model="form.tenant_id" />
        </el-form-item>
        <el-form-item label="Client ID">
          <el-input v-model="form.client_id" />
        </el-form-item>
        <el-form-item label="Client secret">
          <el-input v-model="form.client_secret" type="password" />
        </el-form-item>
        <el-button type="primary" :loading="saving" @click="save">Save</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { createTenant, listTenants } from "../api/endpoints";

const tenants = ref<any[]>([]);
const form = reactive({ display_name: "", tenant_id: "", client_id: "", client_secret: "" });
const saving = ref(false);

async function load() {
  tenants.value = await listTenants();
}

async function save() {
  saving.value = true;
  await createTenant(form);
  saving.value = false;
  await load();
}

onMounted(load);
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
</style>

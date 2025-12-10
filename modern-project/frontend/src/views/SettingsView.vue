<template>
  <div>
    <h3>System toggles</h3>
    <el-form label-position="top" style="max-width: 560px">
      <el-form-item label="WeChat callback indicator">
        <el-input v-model="wxCallback" />
      </el-form-item>
      <el-button type="primary" @click="save">Save</el-button>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { updateSetting } from "../api/endpoints";

const wxCallback = ref("N");

async function save() {
  await updateSetting("WX_CALLBACK_IND", wxCallback.value);
}
</script>

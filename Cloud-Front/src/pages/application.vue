<script setup lang="ts">
import {useUserStore} from "@/stores/user";
import UploadComponent from "@/components/UploadComponent.vue";

const user = useUserStore()
</script>

<template>
  <el-container>
    <el-header  style="position: fixed; width: 100%">
      <MenuComponent page-index="/application"/>
    </el-header>
    <el-main style="margin-top: 10vh">
      <el-card shadow="hover">
        <UploadComponent />
      </el-card>
    </el-main>
  </el-container>
</template>

<style scoped>

</style>
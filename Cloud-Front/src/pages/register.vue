<script setup lang="ts">
import {useUserStore} from "@/stores/user";

const user = useUserStore()
</script>

<template>
  <el-container>
    <el-header  style="position: fixed; width: 100%">
      <MenuComponent page-index="/register"/>
    </el-header>
    <el-main style="margin-top: 10vh">
      <el-card shadow="hover" header="注册信息" v-if="user.username===''">
        <RegisterForm/>
      </el-card>

      <HelloWorld msg="Hello World!" v-if="user.username!==''"/>
    </el-main>
  </el-container>
</template>

<style scoped>

</style>
<script setup lang="ts">

import {useUserStore} from "@/stores/user";
import axios from "axios";
import {SERVER_ADDR} from "@/config";
import {onMounted, ref} from "vue";

const user = useUserStore()
const logAddress = SERVER_ADDR+'/getLog/'+user.username
const log = ref([])

onMounted(() => {
  getLog()
})

function getLog(){
  axios.get(logAddress)
      .then((response) => {
        log.value = response.data
        console.log(log.value)
      })
}

</script>

<template>
  <el-card style="width: 100%">
    <template #header>
      <div class="card-header">
        <span>日志</span>
      </div>
    </template>
    <p v-for="text in log" :key="text" class="text item">{{text}}</p>
  </el-card>
</template>

<style scoped>

</style>
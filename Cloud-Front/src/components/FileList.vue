<script setup lang="tsx">
import {onMounted, ref} from 'vue'
import {useFilesStore} from "@/stores/file"
import {useUserStore} from "@/stores/user";
import {SERVER_ADDR} from "@/config";
import axios from "axios";
import {useRouter} from "vue-router";
import {ElNotification} from "element-plus";


const files = useFilesStore()
const user = useUserStore()
const router = useRouter();
const fileList = ref(files.files)

onMounted(() => {
  files.update(user.username)
  fileList.value = files.files
})

function download(filename){
  const postUrl = SERVER_ADDR+'/download/'+filename+'/'+user.username
  window.open(postUrl)
}

function del(filename){
  const postUrl = SERVER_ADDR+'/delete/'+filename+'/'+user.username
  axios.delete(postUrl)
      .then(response =>{
          files.update(user.username)
          fileList.value = files.files
          router.go(0)
      })

}

const permit = ref("")

function addPermission(filename, username){
  const postUrl = SERVER_ADDR+'/addPermission/'+user.username+'/'+filename+'/'+username
  axios.post(postUrl)
      .then(() => {
        ElNotification({
          offset: 70,
          title: '授权成功',
          duration: 1500
        })
      })
}

function delPermission(filename, username){
  const postUrl = SERVER_ADDR+'/deletePermission/'+user.username+'/'+filename+'/'+username
  axios.post(postUrl)
      .then(() => {
        ElNotification({
          offset: 70,
          title: '撤销授权成功',
          duration: 1500
        })
      })
}

</script>

<template>
  <el-table :data="fileList" style="width: 100%">
    <el-table-column label="文件名称" width="400">
      <template #default="scope">
        <div style="display: flex; align-items: center">
          <span style="margin-left: 10px">{{ scope.row.name }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="下载/删除">
      <template #default="scope">
        <el-button size="small" @click="download(scope.row.name)">下载</el-button>
        <el-button size="small" type="danger" @click="del(scope.row.name)">删除</el-button>
      </template>
    </el-table-column>
    <el-table-column label="授权">
      <template #default="scope">
        <el-input v-model="permit" style="width: 240px;padding-right: 20px" placeholder="输入用户名"/>
        <el-button size="small" @click="addPermission(scope.row.name, permit)">授权</el-button>
        <el-button size="small" @click="delPermission(scope.row.name, permit)">撤销</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<style scoped>

</style>
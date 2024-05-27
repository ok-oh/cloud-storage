<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'
import {useUserStore} from "@/stores/user";

const user = useUserStore()
const uploadAddress = "http://localhost:5000/upload/"+user.username
</script>

<template>
  <el-upload
      class="upload-demo"
      drag
      :action=uploadAddress
      multiple
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      拖入文件 或者 <em>选择文件</em>
    </div>
  </el-upload>
</template>
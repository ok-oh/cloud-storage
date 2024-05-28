<script setup lang="ts">

import {h, reactive, ref} from "vue";
import {ElNotification} from "element-plus";
import {useRouter} from "vue-router";
import axios from "axios";
import {useUserStore} from "@/stores/user";
import {SERVER_ADDR} from "@/config";
import {useFilesStore} from "@/stores/file";

const user = useUserStore();
const files = useFilesStore();
const router = useRouter();
const ruleFormRef = ref()
const ruleForm = reactive({
  username: '',
  password: ''
})

const rules = reactive({
  username: [
    {required: true, message: '此字段为必填项', trigger: 'change'},
    {min: 2, max: 8, message: '用户名长度不符合要求(2-8)', trigger: 'change'},
    {pattern: /^[a-zA-Z\d_]*$/, message: '用户名只能包含字母,数字,下划线', trigger: 'change'}],
  password: [
    {required: true, message: '此字段为必填项', trigger: 'change' },
    {min: 6, max: 12, message: '密码长度不符合要求(6-12)', trigger: 'change'},
    {pattern: /^[\x21-\x7e]*$/, message: '密码只能包含字母,数字和符号', trigger: 'change'},
    {pattern: /^(?=.*[a-zA-Z])(?=.*\d).*$/,
     message: '密码未达到复杂性要求:密码必须包含大小写字母和数字', trigger: 'change'}]
})

const submitForm = async (formEL) => {
  if (!formEL) return
  await formEL.validate(async (valid) => {
    if (!valid) return
    try {
      const response = await axios.get(
          SERVER_ADDR+'/login/'+ruleForm.username+'/'+ruleForm.password
      )
      if(response.data == 'login pass'){
        user.update(ruleForm.username)
        files.update(user.username)
        ElNotification({
          offset: 70,
          title: '登录成功',
          duration: 1500
        })
        await router.push('/')
      }else
      {
          ElNotification({
              offset: 70,
              title: '用户不存在或密码错误',
              duration: 1500
          })
      }
    } catch (error) {
      console.log(error)
      ElNotification({
        offset: 70,
        title: '登录错误',
        duration: 1500
      })
      return
    }
  })
}

</script>

<template>
  <el-form class="demo-ruleForm"
           ref="ruleFormRef"
           :model="ruleForm"
           :rules="rules"
           label-width="120px">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="ruleForm.username" type="text"/>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="ruleForm.password" autocomplete="off" type="password" show-password/>
    </el-form-item>
    <el-row justify="center">
      <el-col :span="12" style="display: flex; justify-content: center; align-items: center">
        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleFormRef)" >
            登录
          </el-button>
        </el-form-item>
      </el-col>
      <el-col :span="12" style="display: flex; justify-content: center; align-items: center">
        <el-form-item>
          <el-button @click="this.$router.push('/register')">
            注册
          </el-button>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
</template>

<style scoped>

</style>
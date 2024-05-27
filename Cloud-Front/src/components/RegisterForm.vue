<script setup lang="ts">
import {ref, reactive} from "vue"
import {ElNotification, type FormInstance} from "element-plus"
import {useRouter} from "vue-router";
import axios from "axios";
import {SERVER_ADDR} from "@/config";

const router = useRouter();
const ruleFormRef = ref()
const validateCheckPass = (rule, value, callback) => {
  if (ruleForm.password === '') return
  if (value !== ruleForm.password) {
    callback(new Error("密码不一致"))
  } else {
    callback()
  }
}

const ruleForm = reactive({
  username: '',
  password: '',
  checkPassword: '',
  rick: false
})

const rules = reactive({
  username: [
    {required: true, message: '此字段为必填项', trigger: 'change' },
    {min: 2, max: 8, message: '用户名长度不符合要求(2-8)', trigger: 'change'},
    {pattern: /^[a-zA-Z\d_]*$/, message: '用户名只能包含字母,数字和下划线', trigger: 'change'}],
  password: [
    {required: true, message: '此字段为必填项', trigger: 'change' },
    {min: 6, max: 12, message: '密码长度不符合要求(6-12)', trigger: 'change'},
    {pattern: /^[\x21-\x7e]*$/, message: '密码只能包含字母,数字和符号', trigger: 'change'},
    {pattern: /^(?=.*[a-zA-Z])(?=.*\d).*$/,
     message: '密码未达到复杂性要求:密码必须包含字母和数字', trigger: 'change'}],
  checkPassword: [
    {required: true, message: '此字段为必填项', trigger: 'change' },
    {validator: validateCheckPass, trigger: 'change'}],
})

const submitForm = async (formEL: FormInstance | undefined) => {
  if (!formEL) return
  await formEL.validate(async (valid) => {
    if (!valid) return
    try {
      const response = await axios.post(
          SERVER_ADDR+'/addNewUser/'+ruleForm.username+'/'+ruleForm.password,
          {
            username: ruleForm.username,
            password: ruleForm.password,
          })
    } catch (error) {
      console.log(error)
      ElNotification({
        offset: 70,
        title: '注册错误',
        duration: 1500
      })
      return
    }

    ElNotification({
      offset: 70,
      title: '注册成功',
      duration: 1500
    })
    await router.push('/login')
  })
}

</script>

<template>
  <el-form ref="ruleFormRef"
           :model="ruleForm"
           :rules="rules"
           class="demo-ruleForm"
           label-width="120px">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="ruleForm.username" type="text"/>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="ruleForm.password" autocomplete="off" type="password"/>
    </el-form-item>
    <el-form-item label="密码确认" prop="checkPassword">
      <el-input v-model="ruleForm.checkPassword" autocomplete="off" type="password"/>
    </el-form-item>
    <el-form-item prop="rick">
      <el-checkbox v-model="ruleForm.rick">
        <span>我已阅读并同意</span>
        <el-link type="primary" href="https://www.bilibili.com/video/BV1GJ411x7h7/" target="_blank">《CloudMemory服务条款》</el-link>
      </el-checkbox>
    </el-form-item>

    <el-row justify="start">
      <el-col :span="12" style="display: flex; justify-content: center; align-items: center">
        <el-form-item>
          <el-button  type="primary" @click="submitForm(ruleFormRef)" :disabled="!ruleForm.rick">
            提交
          </el-button>
        </el-form-item>
      </el-col>
      <el-col :span="7" style="display: flex; justify-content: center; align-items: center">
        <el-form-item>
          <el-button @click="this.$router.back()">
            返回
          </el-button>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
</template>

<style scoped>

</style>
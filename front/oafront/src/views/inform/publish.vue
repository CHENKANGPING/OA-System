<script name="informpublish" setup>
import OAMain from "@/components/OAMain.vue";
import { onBeforeUnmount, onMounted, reactive, ref, shallowRef } from 'vue'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import staffHttp from "@/api/staffHttp.js";
import { ElMessage } from "element-plus";
import { useAuthStore } from "@/stores/auth.js";
import informHttp from "@/api/informHttp.js";


const authStore = useAuthStore()

let informForm = reactive({
  title: '',
  content: '',
  department_ids: []
})

const rules = reactive({
  title: [{ required: true, message: "请输入标题！", trigger: 'blur' }],
  content: [{ required: true, message: "请输入内容！", trigger: 'blur' }],
  department_ids: [{ required: true, message: "请选择部门！", trigger: 'change' }],
})

let formRef = ref()
let formLabelWidth = "100px"
let departments = ref([])


// 这是跟wangEditor相关的配置
const editorRef = shallowRef()
const toolbarConfig = {}
const editorConfig = {
  placeholder: '请输入内容...',
  MENU_CONF: {
    uploadImage: {
      server: import.meta.env.VITE_BASE_URL + '/image/upload',
      fieldName: 'image',
      maxFileSize: 0.5 * 1024 * 1024,
      maxNumberOfFiles: 10,
      allowedFileTypes: ['image/*'],
      headers: {
        Authorization: "JWT " + authStore.token
      },
      timeout: 6 * 1000,
      customInsert(res, insertFn) {
        if (res.erron == 0) {  // 修正：erron 而不是 errno
          let data = res.data
          let url = import.meta.env.VITE_BASE_URL + data.url
          let href = import.meta.env.VITE_BASE_URL + data.href
          let alt = data.alt || '上传的图片'  // 修正：alt 应该是文本，不是 URL
          insertFn(url, alt, href)
        } else {
          ElMessage.error(res.message)
        }
      },
      onFailed(file, res) {
        console.log(`${file.name} 上传失败`, res)
      },

      onError(file, err, res) {
        if (file.size > 0.5 * 1024 * 1024) {
          ElMessage.error('文件大小不能超过 0.5MB')
        } else {
          ElMessage.error('图片格式不正确！')
        }
      },
    }
  }
}
let mode = "default"

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

const handleCreated = (editor) => {
  editorRef.value = editor // 记录 editor 实例，重要！
}
// 这是跟wangEditor相关的配置


const onSubmit = () => {
  formRef.value.validate(async(valid, fields) => {
    if (valid) {
      console.log(informForm);
      try{
        let data =  await informHttp.publishInform(informForm)
        console.log(data);
      }catch(detail){
        ElMessage.error(detail)
      }
    }
  })
}

onMounted(async () => {
  try {
    let data = await staffHttp.getALLDepartment()
    departments.value = data.results
  } catch (detail) {
    ElMessage.error(detail)
  }
})


</script>

<template>
  <OAMain title="发布通知">
    <el-card>
      <el-form ref="formRef" :model="informForm" :rules="rules">
        <el-form-item :label-width="formLabelWidth" label="标题" prop="title">
          <el-input v-model="informForm.title" autocomplete="off" />
        </el-form-item>
        <el-form-item :label-width="formLabelWidth" label="部门可见" prop="department_ids">
          <el-select v-model="informForm.department_ids" multiple>
            <el-option :value="0" label="所有部门"></el-option>
            <el-option v-for="department in departments" :key="department.name" :label="department.name"
              :value="department.id" />
          </el-select>
        </el-form-item>
        <el-form-item :label-width="formLabelWidth" label="内容" prop="content">
          <div style="border: 1px solid #ccc; width: 100%">
            <Toolbar :defaultConfig="toolbarConfig" :editor="editorRef" :mode="mode"
              style="border-bottom: 1px solid #ccc" />
            <Editor v-model="informForm.content" :defaultConfig="editorConfig" :mode="mode"
              style="height: 500px; overflow-y: hidden;" @onCreated="handleCreated" />
          </div>
        </el-form-item>
        <el-form-item>
          <div style="display: flex; justify-content: flex-end; width: 100%;">
            <el-button type="primary" @click="onSubmit">提交</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </OAMain>
</template>

<style scoped></style>
<script setup>
import {ref} from "vue";
// 移除了 defineModel、defineProps 和 defineEmits 的导入

// 定义model:v-model
let dialogVisible = defineModel({required:true});

// 定义属性
let props = defineProps({
  title:{
    type:String,
    default:''
  },
  width:{
    type:String,
    default:'500'
  }
})
// 定义事件
const emits = defineEmits(['cancel','submit'])


const onCancel =() =>{
  dialogVisible.value = false;
  emits('cancel')
}

const onSubmit =() =>{
  emits('submit')
}

</script>

<template>
  <el-dialog v-model="dialogVisible" :title="props.title" :width="props.width">
    <slot></slot>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onCancel">取消</el-button>
        <el-button type="primary" @click="onSubmit">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>
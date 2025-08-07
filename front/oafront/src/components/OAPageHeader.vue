<script name="OAPageHeader" setup>
import router from "@/router/index.js";
// 移除了 defineProps 的导入

const goBack = () => {
  router.go(-1)
}

let props = defineProps({
  content: ""
})

</script>

<template>
  <el-page-header title="返回" @back="goBack">
    <template #content>
      <span class="text-large font-600 mr-3">{{ props.content }}</span>
    </template>
  </el-page-header>
</template>

<style scoped>

</style>
<script setup>
import OAPageHeader from "@/components/OAPageHeader.vue";
// 移除了 defineProps 的导入

let props = defineProps({
  title: ""
})

</script>

<template>
  <el-space direction="vertical" fill style="width: 100%">
    <OAPageHeader :content="props.title"></OAPageHeader>
    <slot></slot>
  </el-space>
</template>

<style scoped>
.el-space :deep(.el-space__item) {
  width: 100%;
}
</style>
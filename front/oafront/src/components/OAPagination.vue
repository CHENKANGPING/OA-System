<script setup name="OAPagination">
// 移除了 defineModel 和 defineProps 的导入

let props = defineProps({
  total:{
    type:Number,
    default:0
  },
  pageSize:{
    type:Number,
    default:10
  }
})

let page = defineModel({required:true})

</script>

<template>
 <el-pagination v-model:current-page="page" :total="props.total"
                       background layout="prev, pager, next"/>
</template>

<style scoped>
.el-pagination {
  justify-content: center;
}
</style>
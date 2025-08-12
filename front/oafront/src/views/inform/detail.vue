<script name="informdetail" setup>
import {onMounted, reactive} from "vue";
import OAMain from "@/components/OAMain.vue";
import informHttp from "@/api/informHttp.js";
import {useRoute} from "vue-router";
import {ElMessage} from "element-plus";
import timeFormatter from "../../utlis/timeFormatter.js";

const route = useRoute()

let inform = reactive({
  title: "",
  content: "",
  create_time: "",
  author: {
    realname: "",
    department: {
      name: ""
    }
  }
})

onMounted(async () => {
  const pk = route.params.pk  // 移到外面
  try {
    let data = await informHttp.getInformDetail(pk)
    Object.assign(inform, data)
  } catch (detail) {
    ElMessage.error(detail)
  }
  
  // 确保阅读记录API调用
  try {
    await informHttp.readInform(pk)
  } catch (error) {
    console.error('记录阅读失败:', error)
  }
})

</script>

<template>
  <OAMain title="通知详情">
    <el-card>
      <template #header>
        <div style="text-align: center">
          <h2 style="padding-bottom: 20px">{{ inform.title }}</h2>
          <div>
            <span style="margin-right: 20px;">作者:{{ inform.author.realname }}</span>
            <span>发布时间：{{ timeFormatter.stringFromDateTime(inform.create_time) }}</span>
          </div>
        </div>
      </template>
      <template #default>
        <div v-html="inform.content" class="content"></div>
      </template>
      <template #footer>
        <div>
          <span>阅读次数：{{inform.read_count}}</span>
        </div>
      </template>
    </el-card>
  </OAMain>
</template>

<style scoped>
.content :deep(img){
  max-width: 100%;
}
</style>
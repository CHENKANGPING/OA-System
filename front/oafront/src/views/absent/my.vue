<script name="myabsent" setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import absentHttp from "@/api/absentHttp.js";
import { ElMessage } from "element-plus";
import timeFormatter from "@/utlis/timeFormatter.js";
import OAMain from "@/components/OAMain.vue";
import OAPagination from "@/components/OAPagination.vue";
import OADialog from "@/components/OADialog.vue";

let formLabelWidth = "100px"
let dialogFormVisible = ref(false)
let absentFrom = reactive({
  title: '',
  absent_type_id: null,
  date_range: [],
  request_content: ""
})
let absent_types = ref([])
let responder = reactive({
  email: '',
  realname: ''
})
let pageination = reactive({
  total: 0,
  page: 1
})

let rules = reactive({
  title: [
    { required: true, message: '请输入标题！', trigger: 'blur' }
  ],
  absent_type_id: [
    { required: true, message: '请选择请假类型！', trigger: 'change' }
  ],
  date_range: [
    { required: true, message: '请选择请假日期！', trigger: 'blur' }
  ],
  request_content: [
    { required: true, message: '请输入请假理由！', trigger: 'blur' }
  ],
})
let absentFromRef = ref()
let responder_str = computed(() => {
  if (responder.email) {
    return '[' + responder.email + ']' + responder.realname
  } else {
    return "无"
  }
})

// 个人考勤信息
let absents = ref([])


const onShowDialog = () => {
  absentFrom.title = ""
  absentFrom.absent_type_id = []
  absentFrom.date_range = []
  absentFrom.request_content = ""  // 改为空字符串
  dialogFormVisible.value = true
}

const onSubmitAbsent = () => {
  absentFromRef.value.validate(async (valid, fields) => {
    if (valid) {
      let data = {
        title: absentFrom.title,
        absent_type_id: absentFrom.absent_type_id,
        start_date: absentFrom.date_range[0],
        end_date: absentFrom.date_range[1],
        request_content: absentFrom.request_content
      }
      try {
        let absent = await absentHttp.applyAbsent(data)
        dialogFormVisible.value = false;
        absents.value.unshift(absent)
        ElMessage.success('发起考勤成功！')
      } catch (detail) {
        ElMessage.error(detail)
      }
    }
  })
}

onMounted(async () => {
  try {
    //1.获取请假类型
    const absent_types_data = await absentHttp.getAbsentTypes()
    absent_types.value = absent_types_data

    //2.获取审批者
    let responder_data = await absentHttp.getResponder()
    Object.assign(responder, responder_data)

    //3.获取个人考勤列表
    await requestAbsents(1)

  } catch (detail) {
    ElMessage.error(detail)

  }
})

watch(() => pageination.page, (value) => {
  requestAbsents(value)
})

const requestAbsents = async (page) => {
  try {
    let absents_data = await absentHttp.getMyAbsents(page)
    let total = absents_data.count;
    pageination.total = total
    let results = absents_data.results;
    absents.value = results

  } catch (detail) {
    ElMessage.error(detail)
  }
}


</script>

<template>
  <OAMain title="个人考勤">
    <el-card style="text-align: right">
      <el-button type="primary" @click="onShowDialog">
        <el-icon>
          <Plus />
        </el-icon>
        发起考勤
      </el-button>
    </el-card>
    <el-card>
      <el-table :data="absents" style="width: 100%">
        <el-table-column label="标题" prop="title" />
        <el-table-column label="类型" prop="absent_type.name" />
        <el-table-column label="原因" prop="request_content" />
        <el-table-column label="发起时间">
          <template #default="scope">
            {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="开始日期" prop="start_date" />
        <el-table-column label="结束日期" prop="end_date" />
        <el-table-column label="审核领导">
          {{ responder_str }}
        </el-table-column>
        <el-table-column label="反馈意见" prop="response_content" />
        <el-table-column label="审核状态">
          <template #default="scope">
            <el-tag v-if="scope.row.status == 1" type="info">审核中</el-tag>
            <el-tag v-else-if="scope.row.status == 2" type="success">已通过</el-tag>
            <el-tag v-else type="danger">已拒绝</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <!--        <el-pagination v-model:current-page="pageination.page" :page-size="1" :total="pageination.total"-->
        <!--                       background layout="prev, pager, next"/>-->
        <OAPagination v-model="pageination.page" :total="pageination.total"></OAPagination>
      </template>
    </el-card>
  </OAMain>

  <OADialog v-model="dialogFormVisible" title="发起请假" @submit="onSubmitAbsent">
    <el-form ref="absentFromRef" :model="absentFrom" :rules="rules">
      <el-form-item :label-width="formLabelWidth" label="标题" prop="title">
        <el-input v-model="absentFrom.title" autocomplete="off" />
      </el-form-item>
      <el-form-item :label-width="formLabelWidth" label="请假类型" prop="absent_type_id">
        <el-select v-model="absentFrom.absent_type_id" placeholder="请选择请假类型">
          <el-option v-for="item in absent_types" :key="item.name" :label="item.name" :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item :label-width="formLabelWidth" label="请假时间" prop="date_range">
        <el-date-picker v-model="absentFrom.date_range" end-placeholder="结束日期" format="YYYY-MM-DD" range-separator="到"
          start-placeholder=起始日期 type="daterange" value-format="YYYY-MM-DD" />
      </el-form-item>
      <el-form-item :label-width="formLabelWidth" label="审批领导">
        <el-input :value="responder_str" autocomplete="off" disabled readonly />
      </el-form-item>
      <el-form-item :label-width="formLabelWidth" label="请假理由" prop="request_content">
        <el-input v-model="absentFrom.request_content" :label-width="formLabelWidth" type="textarea" />
      </el-form-item>
    </el-form>
  </OADialog>
</template>

<style scoped></style>
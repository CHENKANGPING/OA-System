<script name="subabsent" setup>
import timeFormatter from "@/utlis/timeFormatter.js";
import {onMounted, reactive, ref} from "vue";
import OAMain from "@/components/OAMain.vue";
import OAPagination from "@/components/OAPagination.vue";
import absentHttp from "@/api/absentHttp.js";
import {ElMessage} from "element-plus";
import OADialog from "@/components/OADialog.vue";


let absents = ref([])
let pageination = reactive({
  total: 0,
  page: 1
})
let dialogVisible = ref(false)
let absentFrom = reactive({
  status: 2,
  response_content: ""
})
let rules = reactive({
  status: [{required: true, message: '请选择处理结果!', trigger: 'change'}],
  response_content: [{required: true, message: '请输入理由！', trigger: 'blur'}]
})

let absentFromRef = ref()
let handelIndex = null

onMounted(async () => {
  try {
    let data = await absentHttp.getSubAbsent()
    pageination.total = data.count
    absents.value = data.results
  } catch (detail) {
    ElMessage.error(detail)
  }
})

const onShowDialog = (index) => {
  absentFrom.status = 2
  absentFrom.response_content = ""
  dialogVisible.value = true
  handelIndex = index
}

const onSubmitAbsent = () =>{
  absentFromRef.value.validate(async(valid,fields) =>{
    if(valid){
      try{
        dialogVisible.value = false
        const absent = absents.value[handelIndex]
        const data = await absentHttp.handelSubAbsent(absent.id, absentFrom.status, absentFrom.response_content)
        // console.log(data);
        absents.value.splice(handelIndex,1,data)
        ElMessage.success('下属考勤处理成功！')
        
      }catch(detail){
        ElMessage.error(detail)
      }
    }
  })
}


</script>

<template>
  <OADialog v-model="dialogVisible" title="处理考勤" @submit="onSubmitAbsent">
    <el-form ref="absentFromRef" :model="absentFrom" :rules="rules" label-width="100px">
      <el-form-item label="结果" prop="status">
        <el-radio-group v-model="absentFrom.status">
          <el-radio :value="2">通过</el-radio>
          <el-radio :value="3">拒绝</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="理由" prop="response_content">
        <el-input v-model="absentFrom.response_content" type="textarea"/>
      </el-form-item>
    </el-form>
  </OADialog>
  <OAMain title="下属考勤">
    <el-card>
      <el-table :data="absents" style="width: 100%">
        <el-table-column label="标题" prop="title"/>
        <el-table-column label="类型" prop="absent_type.name"/>
        <el-table-column label="原因" prop="request_content"/>
        <el-table-column label="发起时间">
          <template #default="scope">
            {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="开始日期" prop="start_date"/>
        <el-table-column label="结束日期" prop="end_date"/>
        <el-table-column label="审核领导" prop="responder.realname"/>
        <el-table-column label="反馈意见" prop="response_content"/>
        <el-table-column label="审核状态">
          <template #default="scope">
            <el-tag v-if="scope.row.status == 1" type="info">审核中</el-tag>
            <el-tag v-else-if="scope.row.status == 2" type="success">已通过</el-tag>
            <el-tag v-else type="danger">已拒绝</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="处理">
          <template #default="scope">
            <el-button v-if="scope.row.status==1" icon="EditPen" type="primary" @click="onShowDialog(scope.$index)"/>
            <el-button v-else disabled type="default">已处理</el-button>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <OAPagination v-model="pageination.page" :total="pageination.total"></OAPagination>
      </template>
    </el-card>
  </OAMain>
</template>

<style scoped>
.el-pagination {
  justify-content: center;
}

</style>
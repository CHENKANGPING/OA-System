<script name="stafflist" setup>
import OAMain from '@/components/OAMain.vue';
import {onMounted, reactive, ref, watch} from 'vue'
import timeFormatter from '@/utlis/timeFormatter';
import staffHttp from '@/api/staffHttp';
import {ElMessage} from 'element-plus'
import OADialog from '@/components/OADialog.vue';
import {useAuthStore} from '@/stores/auth';

const authStore = useAuthStore()


let staffs = ref([])
let pagination = reactive({
  page: 1,
  total: 0,
})

let page_size = ref(1)
let dialogVisible = ref(false)
let staffForm = reactive({
  status: 1,
})
let handleIndex = 0
let filterForm = reactive({
  department_id: null,
  realname: "",
  date_joined: []

})
let departments = ref([])
let tableRef = ref()
const BASE_URL = import.meta.env.VITE_BASE_URL


async function fetchStaffList(page, page_size) {
  try {
    // 获取员工列表
    let data = await staffHttp.getStaffList(page, page_size, filterForm)
    pagination.total = data.count
    pagination.page = page
    staffs.value = data.results

  } catch (detail) {
    ElMessage.error(detail)
  }
}


onMounted(async () => {
  fetchStaffList(1, page_size.value)

  try {
    let data = await staffHttp.getALLDepartment()
    departments.value = data.results

  } catch (detail) {
    ElMessage.error(detail)
  }

})

watch(() => pagination.page, async function (value) {
  fetchStaffList(value, page_size.value)

})

watch(page_size, function (value) {
  if (pagination.page == 1) {
    fetchStaffList(1, value)
  } else {
    pagination.page = 1

  }


})

const onSubmitEditStaff = async () => {

  let staff = staffs.value[handleIndex]

  try {
    let newstaff = await staffHttp.updateStaffStatus(staff.uid, staffForm.status)
    ElMessage.success('修改成功')
    dialogVisible.value = false
    staffs.value.splice(handleIndex, 1, newstaff)
  } catch (detail) {
    ElMessage.error(detail)
  }
}

const onEditStaff = (index) => {
  handleIndex = index
  dialogVisible.value = true
  let staff = staffs.value[index]
  staffForm.status = staff.status
}

const onSearch = () => {
  fetchStaffList(1, page_size.value)

}

const onDownload = async () => {
  let rows = tableRef.value.getSelectionRows()  // 从 getSelectedRows 改为 getSelectionRows
  if (!rows || rows.length == 0) {
    ElMessage.info('请选择要下载的员工')
    return
  }
  try {
    let response = await staffHttp.dowoloadStaffs(rows.map(row => row.uid))
    let href = URL.createObjectURL(response)
    const a = document.createElement('a')
    a.href = href
    a.setAttribute('download', '员工.xlsx')
    document.body.appendChild(a)
    a.click()
    URL.revokeObjectURL(href)
    document.body.removeChild(a)
    ElMessage.success('下载成功')
  } catch (detail) {
    ElMessage.error(detail)
  }
}

const onUploadSuccess = () => {
  ElMessage.success('上传成功')
  fetchStaffList(1, page_size.value)
}

const onUploadError = (error) => {
  let detail = '上传失败'
  try {
    const text = error?.message || ''
    if (typeof text === 'string' && text.trim().startsWith('{')) {
      const obj = JSON.parse(text)
      detail = obj.detail || detail
    } else if (error?.xhr?.responseText) {
      const resp = error.xhr.responseText
      if (typeof resp === 'string' && resp.trim().startsWith('{')) {
        const obj = JSON.parse(resp)
        detail = obj.detail || detail
      }
    } else if (error?.status) {
      detail = `上传失败（${error.status}）`
    }
  } catch (_) {

  }
  ElMessage.error(detail)
}


</script>


<template>
  <OADialog v-model="dialogVisible" title="修改员工状态" @submit="onSubmitEditStaff">
    <el-form :model="staffForm" label-width="100px">
      <el-form-item label="状态" prop="status">
        <el-radio-group v-model="staffForm.status">
          <el-radio :label="1">激活</el-radio>
          <el-radio :label="3">已锁定</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
  </OADialog>
  <OAMain title="员工列表">
    <el-card>
      <el-form :inline="true" class="my-inline-form">
        <el-form-item label="按部门">
          <el-select v-model="filterForm.department_id">
            <el-option v-for="department in departments" :key="department.name" :label="department.name"
                       :value="department.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="按姓名">
          <el-input v-model="filterForm.realname" placeholder="请输入姓名">
          </el-input>
        </el-form-item>
        <el-form-item label="按入职时间">
          <el-date-picker v-model="filterForm.date_range" end-placeholder="结束日期" format="YYYY-MM-DD"
                          range-separator="到" start-placeholder="起始日期" type="daterange" value-format="YYYY-MM-DD"/>
        </el-form-item>
        <el-form-item>
          <el-button icon="Search" type="primary" @click="onSearch"></el-button>
        </el-form-item>
        <el-form-item>
          <el-button icon="Download" type="danger" @click="onDownload">下载</el-button>
        </el-form-item>
        <el-form-item>
          <el-upload :action="BASE_URL + '/staff/upload'"
                     :auto-upload="true"
                     :headers="{'Authorization': 'JWT ' + authStore.token}"
                     :on-error="onUploadError"
                     :on-success="onUploadSuccess"
                     :show-file-list="false"
                     accept=".xlsx,.xls">
            <el-button icon="Upload" type="danger">上传</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card>
      <el-table ref="tableRef" :data="staffs">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column label="序号" width="60">
          <template #default="scope">
            {{ scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="姓名" prop="realname"></el-table-column>
        <el-table-column label="邮箱" prop="email"></el-table-column>
        <el-table-column label="入职时间">
          <template #default="scope">
            {{ timeFormatter.stringFromDateTime(scope.row.date_joined) }}
          </template>
        </el-table-column>
        <el-table-column label="部门" prop="department.name"></el-table-column>
        <el-table-column label="状态">
          <template #default="scope">
            <el-tag v-if="scope.row.status == 1" type="success">正常</el-tag>
            <el-tag v-else-if="scope.row.status = 2" type="warning">未激活</el-tag>
            <el-tag v-else type="danger">已锁定</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button circle icon="Edit" type="primary" @click="onEditStaff(scope.$index)"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <div style="display: flex; justify-content: space-between;">
          <el-form-item label="每页：">
            <el-select v-model="page_size" size="small" style="width: 100px;">
              <el-option :value="1" label="10条/页"></el-option>
              <el-option :value="2" label="20条/页"></el-option>
            </el-select>
          </el-form-item>
          <el-pagination v-model:currentPage="pagination.page" :page-size="page_size" :total="pagination.total"
                         background layout="prev,pager,next"/>
        </div>
      </template>
    </el-card>
  </OAMain>
</template>

<style scoped>
.my-inline-form .el-input {
  --el-input-width: 140px;
}

.my-inline-form .el-select {
  --el-select-width: 140px;
}

.el-form--inline .el-form-item {
  margin-right: 20px;
}


.el-upload {
  display: inline-block;
  vertical-align: top;
}
</style>
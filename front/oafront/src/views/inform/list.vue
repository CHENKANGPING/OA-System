<script name="informlist" setup>
import OAMain from "@/components/OAMain.vue";
import OAPagination from "@/components/OAPagination.vue";
import timeFormatter from "@/utlis/timeFormatter.js";
import { onMounted, reactive, ref } from "vue";
import { useAuthStore } from "@/stores/auth.js";
import informHttp from "@/api/informHttp.js";
import { ElMessage } from "element-plus";
import OADialog from "@/components/OADialog.vue";




const authStore = useAuthStore()
let informs = ref([])
let pageination = reactive({
  page: 1,
  tota: 0
})

let dialogVisible = ref(false)
let handleIndex = 0

const onShowDialog = (index) => {
  handleIndex = index
  dialogVisible.value = true
}

const onDeleteInform = async () => {
  try {
    let inform = informs.value[handleIndex]
    await informHttp.deleteInform(inform.id)
    informs.value.splice(handleIndex, 1)
    ElMessage.success("删除成功")
    dialogVisible.value = false
  } catch (detail) {
    ElMessage.error(detail)
  }

}

onMounted(async () => {
  try {
    let data = await informHttp.getInformList(1)
    pageination.total = data.count
    informs.value = data.results
  } catch (detail) {
    ElMessage.error(detail)
  }
})

</script>

<template>
  <OADialog v-model="dialogVisible" title="提示" @submit="onDeleteInform">

    <span>您确定删除吗！</span>
  </OADialog>
  <OAMain title="通知列表">
    <el-card>
      <el-table :data="informs" style="width: 100%">
        <el-table-column label="标题">
          <template #default="scope">
            <el-badge v-if="scope.row.reads.length == 0" is-dot class="item">
              <router-link :to="{ name: 'inform_detail', params: { pk: scope.row.id } }">
                {{ scope.row.title }}
              </router-link>
            </el-badge>
            <router-link v-else :to="{ name: 'inform_detail', params: { pk: scope.row.id } }">
              {{ scope.row.title }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="发布者">
          <template #default="scope">
            {{ '[' + scope.row.author.department.name + ']' + scope.row.author.realname }}
          </template>
        </el-table-column>
        <el-table-column label="发布时间">
          <template #default="scope">
            {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="部门可见">
          <template #default="scope">
            <el-tag v-if="scope.row.public" type="success">公开</el-tag>
            <el-tag v-for="department in scope.row.departments" v-else :key="department.name" type="info">
              {{ department.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button v-if="scope.row.author.uid == authStore.user.uid" icon="Delete" type="danger"
              @click="onShowDialog(scope.$index)" />
            <el-button v-else disabled type="default">无</el-button>
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
.el-tag {
  margin-right: 4px;
}

.el-badge {
  margin-right: 4px;
  margin-top: 4px;

}
</style>
<script name="home" setup>
import OAMain from "@/components/OAMain.vue";
import { onMounted, ref, nextTick } from "vue";
import homeHttp from "@/api/homeHttp.js";
import { ElMessage } from "element-plus";
import * as echarts from 'echarts'
import timeFormatter from "@/utlis/timeFormatter.js";

let informs = ref([])
let absents = ref([])

onMounted(async () => {
  try {
    const [informsData, absentsData, departmentData] = await Promise.all([
      homeHttp.getLatestInform(),
      homeHttp.getLatestAbsents(),
      homeHttp.getDepartmentStaffCont()
    ])
    
    informs.value = informsData.slice(0, 8)
    absents.value = absentsData.slice(0, 8)

    let xdatas = []
    let ydatas = []
    for (let row of departmentData) {
      xdatas.push(row.name)
      ydatas.push(row.staff_count)
    }
    
    await nextTick()
    
    var myChart = echarts.init(document.getElementById('department-staff-count'));
    myChart.setOption({
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(50, 50, 50, 0.8)',
        borderColor: '#409EFF',
        borderWidth: 1,
        textStyle: {
          color: '#fff'
        }
      },
      xAxis: {
        data: xdatas,
        axisLabel: {
          color: '#606266',
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#DCDFE6'
          }
        }
      },
      yAxis: {
        axisLabel: {
          color: '#606266',
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#DCDFE6'
          }
        },
        splitLine: {
          lineStyle: {
            color: '#F2F6FC'
          }
        }
      },
      series: [
        {
          name: '员工数量',
          type: 'bar',
          data: ydatas,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#409EFF' },
              { offset: 1, color: '#79BBFF' }
            ]),
            borderRadius: [4, 4, 0, 0]
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#337ECC' },
                { offset: 1, color: '#66B1FF' }
              ])
            }
          }
        }
      ],
      grid: {
        top: 30,
        bottom: 30,
        left: 50,
        right: 30,
        containLabel: true
      }
    });
    
    window.addEventListener('resize', () => {
      myChart.resize()
    })
    
  } catch (detail) {
    ElMessage.error(detail?.message || String(detail))
  }
})
</script>

<template>
  <OAMain title="首页">
    <div class="home-container">
      <!-- 部门员工数量卡片 -->
      <el-card class="chart-card modern-card">
        <template #header>
          <div class="card-header">
            <el-icon class="header-icon"><BarChart /></el-icon>
            <h3 class="card-title">部门员工数量统计</h3>
          </div>
        </template>
        <div 
          id="department-staff-count" 
          class="chart-container"
        ></div>
      </el-card>

      <!-- 通知和请假信息 -->
      <el-row :gutter="20" class="info-row">
        <el-col :span="12">
          <el-card class="info-card modern-card">
            <template #header>
              <div class="card-header">
                <el-icon class="header-icon"><Bell /></el-icon>
                <h3 class="card-title">最新通知</h3>
                <el-badge :value="informs.filter(item => item.reads.length === 0).length" class="notification-badge" />
              </div>
            </template>
            <div class="table-container">
              <el-table 
                :data="informs" 
                size="small"
                :show-header="true"
                class="modern-table"
                :max-height="320"
                stripe
              >
                <el-table-column label="标题" min-width="140">
                  <template #default="scope">
                    <router-link 
                      :to="{ name: 'inform_detail', params: { pk: scope.row.id } }"
                      class="link-text"
                    >
                      <el-icon class="link-icon"><Document /></el-icon>
                      {{ scope.row.title }}
                    </router-link>
                  </template>
                </el-table-column>
                <el-table-column label="发布者" width="90">
                  <template #default="scope">
                    <div class="user-info">
                      <el-avatar :size="24" class="user-avatar">
                        {{ (scope.row.author?.realname || '未知')[0] }}
                      </el-avatar>
                      <span class="user-name">{{ scope.row.author?.realname || '未知' }}</span>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="发布时间" width="100">
                  <template #default="scope">
                    <div class="time-info">
                      <el-icon class="time-icon"><Clock /></el-icon>
                      {{ timeFormatter.stringFromDateTime(scope.row.create_time)?.split(' ')[0] || '-' }}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="状态" width="70">
                  <template #default="scope">
                    <el-tag 
                      :type="scope.row.reads.length > 0 ? 'success' : 'warning'" 
                      size="small"
                      effect="light"
                    >
                      <el-icon class="status-icon">
                        <Check v-if="scope.row.reads.length > 0" />
                        <Warning v-else />
                      </el-icon>
                      {{ scope.row.reads.length > 0 ? '已读' : '未读' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="info-card modern-card full-height-card">
            <template #header>
              <div class="card-header">
                <el-icon class="header-icon"><Calendar /></el-icon>
                <h3 class="card-title">最新请假申请</h3>
                <el-tag size="small" type="info">{{ absents.length }} 条记录</el-tag>
              </div>
            </template>
            <div class="table-container full-height">
              <el-table 
                :data="absents" 
                size="small"
                :show-header="true"
                class="modern-table full-table"
                height="100%"
                stripe
              >
                <el-table-column label="部门" width="90">
                  <template #default="scope">
                    <el-tag size="small" type="primary" effect="light">
                      {{ scope.row.requester?.department?.name || '未知' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="申请人" width="90">
                  <template #default="scope">
                    <div class="user-info">
                      <el-avatar :size="24" class="user-avatar">
                        {{ (scope.row.requester?.realname || '未知')[0] }}
                      </el-avatar>
                      <span class="user-name">{{ scope.row.requester?.realname || '未知' }}</span>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="起始日期" prop="start_date" width="100">
                  <template #default="scope">
                    <div class="date-info">
                      <el-icon class="date-icon"><Calendar /></el-icon>
                      {{ scope.row.start_date }}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="结束日期" prop="end_date" width="100">
                  <template #default="scope">
                    <div class="date-info">
                      <el-icon class="date-icon"><Calendar /></el-icon>
                      {{ scope.row.end_date }}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="申请时间" min-width="100">
                  <template #default="scope">
                    <div class="time-info">
                      <el-icon class="time-icon"><Clock /></el-icon>
                      {{ timeFormatter.stringFromDateTime(scope.row.create_time)?.split(' ')[0] || '-' }}
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </OAMain>
</template>

<style scoped>
.home-container {
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
}

/* 现代化卡片样式 */
.modern-card {
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
  transition: all 0.3s ease;
}

.modern-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.chart-card {
  flex: 0 0 auto;
  margin-bottom: 20px;
  height: 280px;
}

.info-row {
  flex: 1;
  min-height: 0;
}

.info-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.full-height-card {
  height: 100%;
}

/* 卡片头部样式 */
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  font-size: 18px;
  color: #409EFF;
}

.card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  flex: 1;
}

.notification-badge {
  margin-left: auto;
}

/* 图表容器 */
.chart-container {
  width: 100%;
  height: 200px;
  padding: 10px;
}

/* 表格容器 */
.table-container {
  flex: 1;
  overflow: hidden;
}

.table-container.full-height {
  height: 100%;
}

/* 现代化表格样式 */
.modern-table {
  font-size: 12px;
  border-radius: 8px;
  overflow: hidden;
}

.full-table {
  height: 100% !important;
  flex: 1;
}

/* 用户信息样式 */
.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.user-avatar {
  font-size: 12px;
  background: linear-gradient(45deg, #409EFF, #79BBFF);
  color: white;
  font-weight: 500;
}

.user-name {
  font-size: 12px;
  color: #606266;
}

/* 时间和日期信息样式 */
.time-info, .date-info {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.time-icon, .date-icon {
  font-size: 12px;
  color: #C0C4CC;
}

/* 链接样式 */
.link-text {
  color: #409EFF;
  text-decoration: none;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
}

.link-text:hover {
  color: #337ECC;
  text-decoration: none;
}

.link-icon {
  font-size: 12px;
}

/* 状态标签样式 */
.status-icon {
  font-size: 12px;
  margin-right: 2px;
}

/* 深度样式覆盖 */
:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(235, 238, 245, 0.6);
  background: rgba(250, 251, 252, 0.8);
  border-radius: 12px 12px 0 0;
}

:deep(.el-card__body) {
  padding: 16px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

:deep(.full-height-card .el-card__body) {
  overflow: hidden;
}

:deep(.modern-table .el-table__header-wrapper) {
  background: #f8f9fa;
}

:deep(.modern-table .el-table__header th) {
  background: #f8f9fa;
  color: #606266;
  font-weight: 600;
  padding: 10px 0;
  border-bottom: 2px solid #e4e7ed;
}

:deep(.modern-table .el-table__body td) {
  padding: 8px 0;
  border-bottom: 1px solid #f0f2f5;
}

:deep(.modern-table .el-table__row:hover) {
  background-color: rgba(64, 158, 255, 0.04);
}

:deep(.full-table .el-table) {
  height: 100% !important;
}

:deep(.full-table .el-table__body-wrapper) {
  flex: 1 !important;
  max-height: none !important;
  overflow-y: auto;
}

/* 滚动条样式 */
:deep(.el-table__body-wrapper::-webkit-scrollbar) {
  width: 6px;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar-track) {
  background: #f1f1f1;
  border-radius: 3px;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar-thumb) {
  background: #c1c1c1;
  border-radius: 3px;
}

:deep(.el-table__body-wrapper::-webkit-scrollbar-thumb:hover) {
  background: #a8a8a8;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .home-container {
    padding: 16px;
  }
  
  .chart-card {
    height: 260px;
  }
  
  .chart-container {
    height: 180px;
  }
}
</style>
<template>
  <v-container>
  <!-- 标题 -->
  <v-row class="mb-6">
    <v-col>
      <h1 class="text-h4 font-weight-bold">日志记录</h1>
    </v-col>
  </v-row>

  <!-- 搜索和筛选区域 -->
  <v-row class="mb-4 align-center">
    <v-col cols="12" sm="8" md="6">
      <v-autocomplete
        v-model="searchSelectedUser"
        :items="searchUsersList"
        :loading="loadingSearchUsers"
        v-model:search="searchQuery"
        item-title="username"
        item-value="id"
        label="搜索用户名"
        prepend-icon="mdi-magnify"
        return-object
        clearable
        hide-details
        @update:search="searchUsersForTable"
        @update:model-value="handleSearchSelection"
      >
        <template v-slot:selection="{ item }">
          <v-chip class="ma-1">
            {{ item.raw.username }}
            <v-avatar start size="24" class="mr-2">
              <v-img :src="getImageUrl(item.raw.avatar)" cover></v-img>
            </v-avatar>
          </v-chip>
        </template>
        <template v-slot:item="{ props, item }">
          <v-list-item v-bind="props" :title="item.raw.username" :subtitle="item.raw.email">
            <template v-slot:prepend>
              <v-avatar size="24" class="mr-2">
                <v-img :src="getImageUrl(item.raw.avatar)" cover></v-img>
              </v-avatar>
            </template>
          </v-list-item>
        </template>
      </v-autocomplete>
    </v-col>
    <v-col v-if="currentUser?.admin_type === 'software_admin'" cols="12" sm="4" md="3">
      <v-text-field
        v-model="searchSelectedOrg"
        label="搜索组织"
        prepend-icon="mdi-office-building"
        clearable
        hide-details
        @update:model-value="handleSearchSelection"
      ></v-text-field>
    </v-col>
     <!-- spacer 自动填充空位 -->
     <v-spacer></v-spacer>

    <!-- 筛选按钮，始终靠右 -->
    <v-col cols="auto">
      <v-btn color="primary" class="text-none mr-2" prepend-icon="mdi-filter-variant" @click="showFilterDialog = true">
        筛选
      </v-btn>
      <v-btn color="success" class="text-none" prepend-icon="mdi-download" @click="showDownloadDialog = true">
        下载日志
      </v-btn>
    </v-col>
  </v-row>

  <v-card class="elevation-2">
    <v-data-table :headers="headers" :items="logs" class="elevation-0" :items-per-page="pageSize" hover :width="'100%'"
      :loading="loading" hide-default-footer>
      <template v-slot:top>
        <div class="d-flex align-center pa-4">
          <div class="text-caption text-medium-emphasis">
            共 {{ totalLogs }} 条记录
          </div>
        </div>
      </template>

      <template v-slot:item.operation_type="{ item }">
        <v-tooltip :text="item.operation_detail ? JSON.stringify(item.operation_detail, null, 2) : '无详情'">
          <template v-slot:activator="{ props }">
            <v-chip v-bind="props" :color="getOperationTypeColor(item.operation_type)" size="small" class="operation-chip">
              {{ getOperationType(item.operation_type) }}
            </v-chip>
          </template>
        </v-tooltip>
      </template>

      <template v-slot:item.target_type="{ item }">
        <div class="d-flex flex-column align-center">
          <v-chip :color="getModelColor(item.target_type)" size="x-small" class="model-chip mb-1">
            {{ getRelatedModel(item.target_type) }}
          </v-chip>
          <span class="text-caption text-medium-emphasis">ID: {{ item.target_id || '-' }}</span>
        </div>
      </template>

      <template v-slot:item.result="{ item }">
        <v-tooltip :text="item.error_msg || '操作成功'">
          <template v-slot:activator="{ props }">
            <v-icon v-bind="props" :color="item.result === 'success' ? 'success' : 'error'" size="small">
              {{ item.result === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle' }}
            </v-icon>
          </template>
        </v-tooltip>
      </template>

      <template v-slot:item.is_anomaly="{ item }">
        <v-icon :color="item.is_anomaly ? 'error' : 'grey-lighten-1'" size="small">
          {{ item.is_anomaly ? 'mdi-shield-alert' : 'mdi-shield-check' }}
        </v-icon>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-btn
          icon
          variant="text"
          size="small"
          color="primary"
          title="查看详情"
          class="mr-1"
          @click="viewDetail(item)"
        >
          <v-icon>mdi-eye</v-icon>
        </v-btn>
        <v-btn
          icon
          variant="text"
          size="small"
          :color="item.is_anomaly ? 'grey' : 'error'"
          :title="item.is_anomaly ? '取消标记异常' : '标记为异常'"
          @click="toggleAnomaly(item)"
        >
          <v-icon>{{ item.is_anomaly ? 'mdi-shield-off' : 'mdi-shield-alert' }}</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <div class="d-flex align-center justify-center pa-4">
      <div class="d-flex align-center">
        <span class="text-caption mr-2">每页显示</span>
        <v-select v-model="pageSize" :items="[5, 10, 20, 50, 100]" density="compact" variant="outlined" hide-details
          style="width: 100px" @update:model-value="handlePageSizeChange"></v-select>
        <span class="text-caption ml-2">条</span>
      </div>
      <v-pagination v-model="currentPage" :length="totalPages" :total-visible="7" class="ml-4"
        @update:model-value="handlePageChange"></v-pagination>
    </div>
  </v-card>

  <!-- 筛选对话框 -->
  <v-dialog v-model="showFilterDialog" max-width="500">
    <v-card class="elevation-4">
      <v-card-title class="text-h6 font-weight-bold">筛选条件</v-card-title>
      <v-card-text>
        <div class="d-flex flex-column gap-4">
          <v-select v-model="filters.operationType" :items="operationTypeOptions" label="操作类型" clearable
            hide-details></v-select>

          <v-select v-model="filters.targetType" :items="targetTypeOptions" label="目标对象类型" clearable
            hide-details></v-select>

          <v-select v-model="filters.result" :items="resultOptions" label="操作结果" hide-details></v-select>

          <v-select v-model="filters.isAnomaly" :items="anomalyOptions" label="是否异常" hide-details></v-select>

          <v-select v-model="filters.timeRange" :items="timeRangeOptions" label="快速选择时间范围" clearable hide-details
            @update:model-value="handleTimeRangeChange"></v-select>

          <div class="d-flex align-center gap-4">
            <v-text-field v-model="filters.startDate" label="开始时间" type="datetime-local" hide-details density="compact"
              :error-messages="timeError" @update:model-value="handleCustomTimeChange"></v-text-field>
            <v-text-field v-model="filters.endDate" label="结束时间" type="datetime-local" hide-details density="compact"
              :error-messages="timeError" @update:model-value="handleCustomTimeChange"></v-text-field>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey" variant="text" @click="resetFilters">重置</v-btn>
        <v-btn color="primary" @click="applyFilters">应用</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- 下载对话框 -->
  <v-dialog v-model="showDownloadDialog" max-width="500">
    <v-card class="elevation-4">
      <v-card-title class="text-h6 font-weight-bold">下载日志</v-card-title>
      <v-card-text>
        <div class="d-flex flex-column gap-4">
          <v-autocomplete
            v-model="downloadSelectedUsers"
            :items="downloadUsersList"
            :loading="loadingDownloadUsers"
            v-model:search="downloadUserSearch"
            item-title="username"
            item-value="id"
            label="选择用户"
            prepend-icon="mdi-account"
            return-object
            multiple
            clearable
            hide-details
            @update:search="searchUsersForDownload"
            @update:model-value="downloadUserSearch = ''"
          >
            <template v-slot:selection="{ item, index }">
              
            <v-chip v-if="index < 6" class="ma-1">
              {{ item.raw.username }}
              <v-avatar start size="24" class="mr-2">
                <v-img :src="getImageUrl(item.raw.avatar)" cover></v-img>
              </v-avatar>
            </v-chip>
              <span v-if="index === 6" class="text-grey text-caption align-self-center">
                (+{{ downloadSelectedUsers.length - 6 }} others)
              </span>
            </template>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="item.raw.username" :subtitle="item.raw.email">
                <template v-slot:prepend>
                  <v-avatar size="24" class="mr-2">
                    <v-img :src="getImageUrl(item.raw.avatar)" cover></v-img>
                  </v-avatar>
                </template>
              </v-list-item>
            </template>
          </v-autocomplete>

          <v-select v-model="downloadFilters.operationType" :items="operationTypeOptions" label="操作类型" clearable
            hide-details></v-select>

          <v-select v-model="downloadFilters.targetType" :items="targetTypeOptions" label="目标对象类型" clearable
            hide-details></v-select>

          <v-select v-model="downloadFilters.isAnomaly" :items="anomalyOptions" label="是否异常" hide-details></v-select>

          <v-select v-model="downloadFilters.timeRange" :items="timeRangeOptions" label="快速选择时间范围" clearable hide-details
            @update:model-value="handleDownloadTimeRangeChange"></v-select>

          <div class="d-flex align-center gap-4">
            <v-text-field v-model="downloadFilters.startDate" label="开始时间" type="datetime-local" hide-details density="compact"
              :error-messages="downloadTimeError" @update:model-value="handleDownloadCustomTimeChange"></v-text-field>
            <v-text-field v-model="downloadFilters.endDate" label="结束时间" type="datetime-local" hide-details density="compact"
              :error-messages="downloadTimeError" @update:model-value="handleDownloadCustomTimeChange"></v-text-field>
          </div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey" variant="text" @click="resetDownloadFilters">重置</v-btn>
        <v-btn color="success" @click="downloadLogs">下载</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- 日志详情对话框 -->
  <v-dialog v-model="showDetailDialog" max-width="800">
    <v-card v-if="currentLogDetail" class="elevation-4">
      <v-toolbar color="primary" density="compact">
        <v-toolbar-title class="text-subtitle-1 white--text">
          {{ currentLogDetail.title || '日志详情' }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="showDetailDialog = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>

      <v-card-text class="pa-4">
        <!-- 基础信息 -->
        <v-row dense class="mb-4">
          <v-col cols="12" md="6">
            <div class="text-caption text-medium-emphasis">操作用户</div>
            <div class="text-body-1">{{ currentLogDetail.user }} ({{ currentLogDetail.user_role }})</div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="text-caption text-medium-emphasis">操作时间</div>
            <div class="text-body-1">{{ currentLogDetail.operation_time }}</div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="text-caption text-medium-emphasis">IP 地址</div>
            <div class="text-body-1">{{ currentLogDetail.ip_address || '-' }}</div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="text-caption text-medium-emphasis">执行结果</div>
            <v-chip :color="currentLogDetail.result === 'success' ? 'success' : 'error'" size="x-small">
              {{ currentLogDetail.result === 'success' ? '成功' : '失败' }}
            </v-chip>
          </v-col>
        </v-row>

        <v-divider class="my-4"></v-divider>

        <!-- 动态详情区域 -->
        <h3 class="text-h6 mb-3">{{ currentLogDetail.title }}</h3>
        
        <!-- 表格形式展示字段 -->
        <v-table density="compact" class="border rounded">
          <tbody>
            <tr v-for="(field, index) in currentLogDetail.fields" :key="index">
              <td class="bg-grey-lighten-4 font-weight-bold" style="width: 140px">{{ field.label }}</td>
              <td>{{ field.value }}</td>
            </tr>
          </tbody>
        </v-table>

        <!-- AI 检测特有结果展示 -->
        <div v-if="currentLogDetail.display_type === 'ai_result' && currentLogDetail.ai_extra" class="mt-6">
          <h3 class="text-h6 mb-3">检测结果概览</h3>
          <v-row>
            <v-col v-for="res in currentLogDetail.ai_extra.results" :key="res.image_id" cols="12" sm="6" md="4">
              <v-card variant="outlined" class="pa-2">
                <v-img :src="getImageUrl(res.image_url)" height="120" cover class="rounded bg-grey-lighten-2 mb-2">
                  <template v-slot:placeholder>
                    <v-row class="fill-height ma-0" align="center" justify="center">
                      <v-icon color="grey-lighten-1">mdi-image-off</v-icon>
                    </v-row>
                  </template>
                </v-img>
                <div class="d-flex justify-space-between align-center">
                  <v-chip :color="res.is_fake ? 'error' : 'success'" size="x-small">
                    {{ res.is_fake ? '疑似造假' : '正常' }}
                  </v-chip>
                  <span class="text-caption font-weight-bold">{{ res.confidence }}</span>
                </div>
                <div v-if="res.llm_judgment" class="text-caption text-truncate mt-1" :title="res.llm_judgment">
                  {{ res.llm_judgment }}
                </div>
              </v-card>
            </v-col>
          </v-row>
          <div v-if="currentLogDetail.ai_extra.more_results" class="text-center mt-4 text-caption text-medium-emphasis">
            仅展示部分检测结果，完整信息请前往检测任务详情页查看。
          </div>
        </div>

        <!-- 错误消息 -->
        <v-alert v-if="currentLogDetail.error_msg" type="error" variant="tonal" class="mt-4" density="compact">
          <div class="text-caption font-weight-bold">错误详情：</div>
          <div class="text-caption">{{ currentLogDetail.error_msg }}</div>
        </v-alert>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="text" @click="showDetailDialog = false">关闭</v-btn>
      </v-card-actions>
    </v-card>
    
    <!-- 加载状态 -->
    <v-card v-else class="pa-10 text-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <div class="mt-4 text-medium-emphasis">正在获取详情...</div>
    </v-card>
  </v-dialog>
</v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSnackbarStore } from '@/stores/snackbar'
import logApi from '@/api/log'
import userApi from '@/api/user'
import axios from 'axios'

const snackbar = useSnackbarStore()

interface Log {
  id: number
  user_id: number
  user: string
  user_role: string
  organization: string
  operation_type: string
  target_type: string
  target_id: number
  operation_detail: any
  ip_address: string
  result: string
  error_msg: string
  is_anomaly: boolean
  operation_time: string
}

interface User {
  id: number
  username: string
  email: string
  avatar: string
}

const headers = computed(() => {
  const baseHeaders = [
    { title: '操作用户', key: 'user', align: 'start' },
    { title: '操作类型', key: 'operation_type', align: 'center' },
    { title: '目标对象', key: 'target_type', align: 'center' },
    { title: '结果', key: 'result', align: 'center' },
    { title: 'IP地址', key: 'ip_address', align: 'center' },
    { title: '异常', key: 'is_anomaly', align: 'center' },
    { title: '操作时间', key: 'operation_time', align: 'center' },
    { title: '操作', key: 'actions', align: 'center', sortable: false },
  ]
  
  if (currentUser.value?.admin_type === 'software_admin') {
    baseHeaders.splice(1, 0, { title: '所属组织', key: 'organization', align: 'start' })
  }
  
  return baseHeaders
}) as any

// 分页相关
const logs = ref<Log[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalLogs = ref(0)
const totalPages = ref(1)

// 表格搜索相关
const searchSelectedUser = ref<User | null>(null)
const searchSelectedOrg = ref<string | null>(null)
const searchUsersList = ref<User[]>([])
const loadingSearchUsers = ref(false)
const searchQuery = ref('')

// 筛选相关
const showFilterDialog = ref(false)
const filters = ref<{
  operationType: string | null
  targetType: string | null
  result: string | null
  isAnomaly: boolean | null
  timeRange: string | null
  startDate: string | null
  endDate: string | null
}>({
  operationType: null,
  targetType: null,
  result: null,
  isAnomaly: null,
  timeRange: null,
  startDate: null,
  endDate: null
})

const operationTypeOptions = [
  { title: '用户登录', value: 'login' },
  { title: '用户登出', value: 'logout' },
  { title: '上传文件', value: 'upload' },
  { title: 'AI检测', value: 'ai_detect' },
  { title: '发起审核', value: 'audit_submit' },
  { title: '执行审核', value: 'audit_op' },
  { title: '实体创建', value: 'entity_create' },
  { title: '实体删除', value: 'entity_delete' },
  { title: '实体更新', value: 'entity_update' },
  { title: '异常标记', value: 'mark_anomaly' }
]

const targetTypeOptions = [
  { title: '用户', value: 'User' },
  { title: '文件管理', value: 'FileManagement' },
  { title: '检测任务', value: 'DetectionTask' },
  { title: '审核请求', value: 'ReviewRequest' },
  { title: '人工审核', value: 'ManualReview' },
  { title: '模型', value: 'Model' }
]

const resultOptions = [
  { title: '全部', value: null },
  { title: '成功', value: 'success' },
  { title: '失败', value: 'failure' }
]

const anomalyOptions = [
  { title: '全部', value: null },
  { title: '仅异常', value: true },
  { title: '正常', value: false }
]

const getImageUrl =(url:string)=>{
  return import.meta.env.VITE_API_URL + url
}


const timeRangeOptions = [
  { title: '最近一天', value: '1d' },
  { title: '最近一周', value: '7d' },
  { title: '最近一月', value: '30d' },
  { title: '最近三月', value: '90d' },
  { title: '最近一年', value: '365d' }
]

// 时间验证相关
const timeError = ref('')

// 处理快速选择时间范围变化
const handleTimeRangeChange = (value: string | null) => {
  if (value) {
    filters.value.startDate = null
    filters.value.endDate = null
    timeError.value = ''
  }
}

// 处理自定义时间变化
const handleCustomTimeChange = () => {
  filters.value.timeRange = null

  if (!filters.value.startDate || !filters.value.endDate) {
    timeError.value = '开始时间和结束时间不能为空'
    return
  }

  const startTime = new Date(filters.value.startDate).getTime()
  const endTime = new Date(filters.value.endDate).getTime()

  if (startTime >= endTime) {
    timeError.value = '开始时间必须早于结束时间'
  } else {
    timeError.value = ''
  }
}

// 重置筛选条件
const resetFilters = () => {
  filters.value = {
    operationType: null,
    targetType: null,
    result: null,
    isAnomaly: null,
    timeRange: null,
    startDate: null,
    endDate: null
  }
  searchSelectedUser.value = null
  searchSelectedOrg.value = null
  timeError.value = ''
  currentPage.value = 1
  pageSize.value = 10
  fetchLogs(1, 10)
  showFilterDialog.value = false
}

// 应用筛选条件
const applyFilters = () => {
  if (timeError.value) {
    return
  }

  currentPage.value = 1
  pageSize.value = 10
  fetchLogs(1, 10)
  showFilterDialog.value = false
}

// 从后端获取日志数据
const fetchLogs = async (page: number, pageSize: number) => {
  loading.value = true
  try {
    // 计算时间筛选
    let startTimeFilter: string | undefined
    let endTimeFilter: string | undefined
    if (filters.value.timeRange) {
      const now = Date.now()
      const ranges: Record<string, number> = {
        '1d': 24 * 60 * 60 * 1000,
        '7d': 7 * 24 * 60 * 60 * 1000,
        '30d': 30 * 24 * 60 * 60 * 1000,
        '90d': 90 * 24 * 60 * 60 * 1000,
        '365d': 365 * 24 * 60 * 60 * 1000
      }
      const rangeMs = ranges[filters.value.timeRange as keyof typeof ranges]
      startTimeFilter = formatDateFilter(now - rangeMs)
      endTimeFilter = formatDateFilter(now)
    } else if (filters.value.startDate && filters.value.endDate) {
      startTimeFilter = formatDateFilter(new Date(filters.value.startDate).getTime())
      endTimeFilter = formatDateFilter(new Date(filters.value.endDate).getTime())
    }

    const params = {
      page,
      page_size: pageSize,
      query: searchSelectedUser.value?.username || '',
      organization: searchSelectedOrg.value || '',
      operation_type: filters.value.operationType || '',
      target_type: filters.value.targetType || '',
      result: filters.value.result || '',
      is_anomaly: filters.value.isAnomaly === null ? undefined : filters.value.isAnomaly,
      startTime: startTimeFilter,
      endTime: endTimeFilter
    }
    const response = await logApi.getLogs(params as any)
    const { data } = response

    if (data && data.logs) {
      logs.value = data.logs
      currentPage.value = data.current_page
      totalPages.value = data.total_pages
      totalLogs.value = data.total_logs
    } else {
      logs.value = []
      currentPage.value = 1
      totalPages.value = 1
      totalLogs.value = 0
    }
  } catch (error) {
    console.error('获取日志数据失败:', error)
    snackbar.showMessage('获取日志数据失败', 'error')
  } finally {
    loading.value = false
  }
}

// 处理页码变化
const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchLogs(page, pageSize.value)
}

// 处理每页数量变化
const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchLogs(1, size)
}

// 时间格式化，用于筛选条件
const formatDateFilter = (timestamp: number) => {
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}


const getOperationType = (type: string) => {
  const option = operationTypeOptions.find(opt => opt.value === type)
  return option ? option.title : type
}

const getRelatedModel = (model: string) => {
  const option = targetTypeOptions.find(opt => opt.value === model)
  return option ? option.title : model
}

const getOperationTypeColor = (type: string) => {
  switch (type) {
    case 'login':
    case 'logout':
      return 'grey'
    case 'upload':
      return 'info'
    case 'ai_detect':
    case 'detection':
      return 'success'
    case 'audit_submit':
    case 'review_request':
      return 'warning'
    case 'audit_op':
    case 'manual_review':
      return 'primary'
    case 'entity_create':
      return 'teal'
    case 'entity_delete':
      return 'red'
    case 'entity_update':
      return 'orange'
    default:
      return 'grey'
  }
}

const getModelColor = (model: string) => {
  switch (model) {
    case 'User':
      return 'brown'
    case 'DetectionTask':
      return 'info'
    case 'FileManagement':
      return 'primary'
    case 'ReviewRequest':
      return 'warning'
    case 'ManualReview':
      return 'success'
    default:
      return 'grey'
  }
}

const toggleAnomaly = async (log: Log) => {
  try {
    const newStatus = !log.is_anomaly
    await logApi.markAnomaly(log.id, newStatus)
    log.is_anomaly = newStatus
    snackbar.showMessage(newStatus ? '已标记为异常' : '已取消异常标记', 'success')
  } catch (error) {
    console.error('切换异常状态失败:', error)
    snackbar.showMessage('操作失败', 'error')
  }
}


// 当前用户
const currentUser = ref<{ 
  email: string;
  admin_type?: string;
} | null>(null)



// 初始化
onMounted(async () => {
  try {
    const res = await userApi.getUserInfo()
    currentUser.value = res.data
  } catch (error) {
    console.error('获取当前用户信息失败:', error)
  }
  fetchLogs(currentPage.value, pageSize.value)
})

const showDownloadDialog = ref(false)
const downloadFilters = ref<{
  operationType: string | null
  targetType: string | null
  isAnomaly: boolean | null
  timeRange: string | null
  startDate: string | null
  endDate: string | null
}>({
  operationType: null,
  targetType: null,
  isAnomaly: null,
  timeRange: null,
  startDate: null,
  endDate: null
})

// 日志详情相关
const showDetailDialog = ref(false)
const currentLogDetail = ref<any>(null)
const loadingDetail = ref(false)

const viewDetail = async (log: Log) => {
  showDetailDialog.value = true
  currentLogDetail.value = null
  loadingDetail.value = true
  try {
    const response = await logApi.getLogDetail(log.id)
    currentLogDetail.value = response.data
  } catch (error) {
    console.error('获取日志详情失败:', error)
    snackbar.showMessage('获取日志详情失败', 'error')
    showDetailDialog.value = false
  } finally {
    loadingDetail.value = false
  }
}

const downloadTimeError = ref('')

// 处理下载时间范围变化
const handleDownloadTimeRangeChange = (value: string | null) => {
  if (value) {
    downloadFilters.value.startDate = null
    downloadFilters.value.endDate = null
    downloadTimeError.value = ''
  }
}

// 处理下载自定义时间变化
const handleDownloadCustomTimeChange = () => {
  downloadFilters.value.timeRange = null

  if (!downloadFilters.value.startDate || !downloadFilters.value.endDate) {
    downloadTimeError.value = '开始时间和结束时间不能为空'
    return
  }

  const startTime = new Date(downloadFilters.value.startDate).getTime()
  const endTime = new Date(downloadFilters.value.endDate).getTime()

  if (startTime >= endTime) {
    downloadTimeError.value = '开始时间必须早于结束时间'
  } else {
    downloadTimeError.value = ''
  }
}

// 重置下载筛选条件
const resetDownloadFilters = () => {
  downloadFilters.value = {
    operationType: null,
    targetType: null,
    isAnomaly: null,
    timeRange: null,
    startDate: null,
    endDate: null
  }
  downloadSelectedUsers.value = []
  downloadTimeError.value = ''
  showDownloadDialog.value = false
}

// 下载相关
const downloadSelectedUsers = ref<User[]>([])
const downloadUsersList = ref<User[]>([])
const loadingDownloadUsers = ref(false)
const downloadUserSearch = ref('')

// 搜索用户（用于下载）
const searchUsersForDownload = async (query: string) => {
  if (!query) {
    downloadUsersList.value = []
    return
  }
  
  loadingDownloadUsers.value = true
  try {
    const response = await userApi.getUsers({ query, page: 1, page_size: 10 })
    downloadUsersList.value = response.data.users || []
  } catch (error) {
    console.error('搜索用户失败:', error)
    snackbar.showMessage('搜索用户失败', 'error')
  } finally {
    loadingDownloadUsers.value = false
  }
}

// 下载日志
const downloadLogs = async () => {
  if (downloadTimeError.value) {
    return
  }

  try {
    // 计算时间筛选
    let startTimeFilter: string | undefined
    let endTimeFilter: string | undefined
    if (downloadFilters.value.timeRange) {
      const now = Date.now()
      const ranges: Record<string, number> = {
        '1d': 24 * 60 * 60 * 1000,
        '7d': 7 * 24 * 60 * 60 * 1000,
        '30d': 30 * 24 * 60 * 60 * 1000,
        '90d': 90 * 24 * 60 * 60 * 1000,
        '365d': 365 * 24 * 60 * 60 * 1000
      }
      const rangeMs = ranges[downloadFilters.value.timeRange as keyof typeof ranges]
      startTimeFilter = formatDateFilter(now - rangeMs)
      endTimeFilter = formatDateFilter(now)
    } else if (downloadFilters.value.startDate && downloadFilters.value.endDate) {
      startTimeFilter = formatDateFilter(new Date(downloadFilters.value.startDate).getTime())
      endTimeFilter = formatDateFilter(new Date(downloadFilters.value.endDate).getTime())
    }

    const params = {
      query: downloadSelectedUsers.value.map(user => user.id),
      operation_type: downloadFilters.value.operationType || '',
      target_type: downloadFilters.value.targetType || '',
      is_anomaly: downloadFilters.value.isAnomaly === null ? undefined : downloadFilters.value.isAnomaly,
      startTime: startTimeFilter,
      endTime: endTimeFilter
    }

    const response = await logApi.downloadLogs(params)
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `logs.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    snackbar.showMessage('日志下载成功', 'success')
    showDownloadDialog.value = false
  } catch (error) {
    console.error('下载日志失败:', error)
    snackbar.showMessage('下载日志失败', 'error')
  }
}

// 处理搜索选择
const handleSearchSelection = () => {
  searchQuery.value = ''
  fetchLogs(currentPage.value, pageSize.value)
}

// 搜索用户（用于表格）
const searchUsersForTable = async (query: string) => {
  if (!query) {
    searchUsersList.value = []
    return
  }
  
  loadingSearchUsers.value = true
  try {
    const response = await userApi.getUsers({ query, page: 1, page_size: 10})
    searchUsersList.value = response.data.users || []
  } catch (error) {
    console.error('搜索用户失败:', error)
    snackbar.showMessage('搜索用户失败', 'error')
  } finally {
    loadingSearchUsers.value = false
  }
}
</script>

<style scoped>
.v-card {
  border-radius: 12px;
  overflow: hidden;
}

.operation-chip {
  font-size: 12px;
  padding: 0 12px;
  font-weight: 500;
}

.model-chip {
  font-size: 12px;
  padding: 0 12px;
  font-weight: 500;
}

:deep(.v-data-table) {
  border-radius: 12px;
  width: 100%;
}

:deep(.v-data-table-header) {
  background-color: rgb(var(--v-theme-surface-variant));
}

:deep(.v-data-table-header th) {
  font-weight: 600;
  font-size: 14px;
  color: rgb(var(--v-theme-on-surface));
  white-space: nowrap;
}

:deep(.v-data-table__tr td) {
  white-space: nowrap;
}

:deep(.v-data-table__tr:hover) {
  background-color: rgba(var(--v-theme-on-surface), 0.04);
}

:deep(.v-chip) {
  font-weight: 500;
}

.search-input {
  max-width: 400px;
}

:deep(.v-text-field .v-field__input) {
  min-height: 40px;
}

:deep(.v-btn--variant-outlined) {
  border-color: rgb(var(--v-theme-outline));
}

:deep(.v-select .v-field__input) {
  min-height: 40px;
}

:deep(.v-select .v-field__append-inner) {
  padding-top: 0;
}

.rounded-circle {
  border-radius: 50% !important;
}

:deep(.v-avatar) {
  overflow: hidden;
  border-radius: 50%;
}

:deep(.v-avatar .v-img) {
  height: 100%;
  width: 100%;
  object-fit: cover;
}
</style>

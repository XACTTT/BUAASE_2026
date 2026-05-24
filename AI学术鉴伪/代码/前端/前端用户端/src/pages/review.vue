<template>
  <div class="review-page">
    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold">我的审核任务</h1>
      </v-col>
    </v-row>

    <v-row class="mb-4">
      <v-col cols="12" sm="8" md="6">
        <v-text-field
          v-model="searchQuery"
          label="搜索发布者"
          append-inner-icon="mdi-magnify"
          clearable
          density="compact"
          hide-details
          class="search-input"
          placeholder="请输入发布者名称"
          @keyup.enter="handleSearch"
          @click:append-inner="handleSearch"
          @click:clear="handleSearch"
        />
      </v-col>
      <v-col cols="12" sm="4" md="6" class="d-flex justify-end">
        <v-btn color="primary" class="text-none mr-2" prepend-icon="mdi-filter-variant" @click="showFilterDialog = true">
          筛选
        </v-btn>
      </v-col>
    </v-row>

    <v-card class="elevation-2">
      <v-data-table
        :headers="headers"
        :items="tasks"
        :items-per-page="pageSize"
        :loading="loading"
        class="elevation-0"
        hover
        hide-default-footer
      >
        <template #top>
          <div class="d-flex align-center pa-4">
            <div class="text-caption text-medium-emphasis">共 {{ totalTasks }} 条记录</div>
          </div>
        </template>

        <template #item.publisher_avatar="{ item }">
          <v-avatar size="40">
            <v-img :src="item.publisher_avatar || fallbackAvatar" :alt="item.publisher_username" />
          </v-avatar>
        </template>

        <template #item.task_type="{ item }">
          <v-chip :color="getTaskTypeColor(item.task_type)" size="small" class="status-chip">
            {{ getTaskTypeName(item.task_type) }}
          </v-chip>
        </template>

        <template #item.status="{ item }">
          <v-chip :color="getStatusColor(item.status)" size="small" class="status-chip">
            {{ getStatusName(item.status) }}
          </v-chip>
        </template>

        <template #item.actions="{ item }">
          <v-btn icon variant="text" size="small" color="primary" class="mr-2" @click="goToTaskDetail(item)">
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
      </v-data-table>

      <div class="d-flex align-center justify-center pa-4">
        <div class="d-flex align-center">
          <span class="text-caption mr-2">每页显示</span>
          <v-select
            v-model="pageSize"
            :items="[5, 10, 20, 50, 100]"
            density="compact"
            variant="outlined"
            hide-details
            style="width: 100px"
            @update:model-value="handlePageSizeChange"
          />
          <span class="text-caption ml-2">条</span>
        </div>
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="7"
          class="ml-4"
          @update:model-value="handlePageChange"
        />
      </div>
    </v-card>

    <v-dialog v-model="showFilterDialog" max-width="500">
      <v-card class="elevation-4">
        <v-card-title class="text-h6 font-weight-bold">筛选条件</v-card-title>
        <v-card-text>
          <div class="d-flex flex-column ga-4">
            <v-select
              v-model="filters.status"
              :items="statusOptions"
              label="任务状态"
              clearable
              hide-details
            />

            <v-select
              v-model="filters.timeRange"
              :items="timeRangeOptions"
              label="快速选择时间范围"
              clearable
              hide-details
              @update:model-value="handleTimeRangeChange"
            />

            <div class="d-flex align-center ga-4">
              <v-text-field
                v-model="filters.startDate"
                label="开始时间"
                type="datetime-local"
                hide-details
                density="compact"
                :error-messages="timeError"
                @update:model-value="handleCustomTimeChange"
              />
              <v-text-field
                v-model="filters.endDate"
                label="结束时间"
                type="datetime-local"
                hide-details
                density="compact"
                :error-messages="timeError"
                @update:model-value="handleCustomTimeChange"
              />
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="resetFilters">重置</v-btn>
          <v-btn color="primary" @click="applyFilters">应用</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import reviewerApi from '@/api/reviewer'
import { useSnackbarStore } from '@/stores/snackbar'

interface Task {
  manual_review_id: number
  manual_review_time: string
  publisher_username: string
  publisher_avatar: string
  resource_count: number
  task_type?: string
  status: string
}

const router = useRouter()
const snackbar = useSnackbarStore()
const fallbackAvatar = 'https://randomuser.me/api/portraits/lego/1.jpg'

const headers = [
  { title: '头像', key: 'publisher_avatar', align: 'center', sortable: false },
  { title: '发布者', key: 'publisher_username', align: 'start' },
  { title: '材料数量', key: 'resource_count', align: 'start' },
  { title: '任务类型', key: 'task_type', align: 'center' },
  { title: '状态', key: 'status', align: 'center' },
  { title: '提交时间', key: 'manual_review_time', align: 'center' },
  { title: '操作', key: 'actions', align: 'center', sortable: false }
] as const

const tasks = ref<Task[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalTasks = ref(0)
const totalPages = ref(1)
const searchQuery = ref('')
const showFilterDialog = ref(false)
const timeError = ref('')

const filters = ref<{
  status: string | null
  timeRange: string | null
  startDate: string | null
  endDate: string | null
}>({
  status: null,
  timeRange: null,
  startDate: null,
  endDate: null
})

const statusOptions = [
  { title: '未完成', value: 'undo' },
  { title: '已完成', value: 'completed' }
]

const timeRangeOptions = [
  { title: '最近一天', value: '1d' },
  { title: '最近一周', value: '7d' },
  { title: '最近一月', value: '30d' },
  { title: '最近三月', value: '90d' },
  { title: '最近一年', value: '365d' }
]

const getStatusColor = (status: string) => {
  if (status === 'undo') return 'error'
  if (status === 'completed') return 'success'
  return 'grey'
}

const getStatusName = (status: string) => {
  if (status === 'undo') return '未完成'
  if (status === 'completed') return '已完成'
  return status || '未知'
}

const getTaskTypeColor = (taskType?: string) => {
  switch (taskType) {
    case 'image':
      return 'blue'
    case 'paper_text':
      return 'green'
    case 'review_text':
      return 'orange'
    case 'multi_material':
      return 'purple'
    default:
      return 'grey'
  }
}

const getTaskTypeName = (taskType?: string) => {
  switch (taskType) {
    case 'image':
      return '图片检测'
    case 'paper_text':
      return '论文检测'
    case 'review_text':
      return 'Review检测'
    case 'multi_material':
      return '多材料检测'
    default:
      return taskType || '未知'
  }
}

const goToTaskDetail = (task: Task) => {
  router.push(`/task/detail/${task.manual_review_id}`)
}

const handleTimeRangeChange = (value: string | null) => {
  if (value) {
    filters.value.startDate = null
    filters.value.endDate = null
    timeError.value = ''
  }
}

const handleCustomTimeChange = () => {
  filters.value.timeRange = null
  if (!filters.value.startDate || !filters.value.endDate) {
    timeError.value = ''
    return
  }

  const startTime = new Date(filters.value.startDate).getTime()
  const endTime = new Date(filters.value.endDate).getTime()
  timeError.value = startTime >= endTime ? '开始时间必须早于结束时间' : ''
}

const resetFilters = () => {
  filters.value = {
    status: null,
    timeRange: null,
    startDate: null,
    endDate: null
  }
  timeError.value = ''
  currentPage.value = 1
  pageSize.value = 10
  fetchTasks(1, 10)
  showFilterDialog.value = false
}

const applyFilters = () => {
  if (timeError.value) return
  currentPage.value = 1
  pageSize.value = 10
  fetchTasks(1, 10)
  showFilterDialog.value = false
}

const handleSearch = () => {
  currentPage.value = 1
  fetchTasks(1, pageSize.value)
}

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

const buildTimeFilters = () => {
  if (filters.value.timeRange) {
    const now = Date.now()
    const ranges: Record<string, number> = {
      '1d': 24 * 60 * 60 * 1000,
      '7d': 7 * 24 * 60 * 60 * 1000,
      '30d': 30 * 24 * 60 * 60 * 1000,
      '90d': 90 * 24 * 60 * 60 * 1000,
      '365d': 365 * 24 * 60 * 60 * 1000
    }
    const rangeMs = ranges[filters.value.timeRange]
    return {
      start_time: formatDateFilter(now - rangeMs),
      end_time: formatDateFilter(now)
    }
  }

  if (filters.value.startDate && filters.value.endDate) {
    return {
      start_time: formatDateFilter(new Date(filters.value.startDate).getTime()),
      end_time: formatDateFilter(new Date(filters.value.endDate).getTime())
    }
  }

  return {}
}

const normalizeAvatar = (avatar?: string) => {
  if (!avatar) return ''
  if (/^https?:\/\//i.test(avatar)) return avatar
  return `http://122.9.45.122${avatar}`
}

const fetchTasks = async (page: number, size: number) => {
  loading.value = true
  try {
    const response = await reviewerApi.getReviewerTasks({
      page,
      page_size: size,
      query: searchQuery.value || '',
      status: filters.value.status || '',
      ...buildTimeFilters()
    })
    const { results = [], current_page = page, total_pages = 1, total_users = 0 } = response.data || {}

    tasks.value = results.map((task: any) => {
      const taskType = task.task_type || 'image'
      const resourceCount = taskType.includes('text') ? (task.text_count || 0) : (task.image_count || 0)
      return {
        manual_review_id: task.manual_review_id,
        manual_review_time: task.manual_review_time,
        publisher_username: task.publisher_username,
        publisher_avatar: normalizeAvatar(task.publisher_avatar),
        resource_count: resourceCount,
        task_type: taskType,
        status: task.status
      }
    })

    currentPage.value = current_page
    totalPages.value = total_pages
    totalTasks.value = total_users
  } catch (error) {
    console.error('获取任务列表失败:', error)
    snackbar.showMessage('获取任务列表失败', 'error')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchTasks(page, pageSize.value)
}

const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchTasks(1, size)
}

onMounted(() => {
  fetchTasks(currentPage.value, pageSize.value)
})
</script>

<style scoped>
.v-card {
  border-radius: 8px;
  overflow: hidden;
}

.status-chip {
  font-size: 12px;
  padding: 0 12px;
  font-weight: 500;
}

.v-btn.v-btn--size-small {
  width: 32px;
  height: 32px;
  padding: 0;
  border-radius: 8px;
}

.v-btn--icon.v-btn--size-small .v-icon {
  font-size: 18px;
}

:deep(.v-data-table) {
  border-radius: 8px;
  width: 100%;
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

.search-input {
  max-width: 400px;
}

:deep(.v-text-field .v-field__input),
:deep(.v-select .v-field__input) {
  min-height: 40px;
}
</style>

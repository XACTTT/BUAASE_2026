<template>
  <div class="review-page">
      <!-- 鏍囬 -->
      <v-row class="mb-6">
        <v-col>
          <h1 class="text-h4 font-weight-bold">鎴戠殑浠诲姟</h1>
        </v-col>
      </v-row>

      <!-- 鎼滅储鏍忓拰绛涢€夋寜閽?-->
      <v-row class="mb-4">
        <v-col cols="12" sm="8" md="6">
          <v-text-field
            v-model="searchQuery"
            label="搜索出版社"
            append-inner-icon="mdi-magnify"
            clearable
            density="compact"
            hide-details
            class="search-input"
            @keyup.enter="handleSearch"
            @click:append-inner="handleSearch"
            @click:clear="handleSearch"
            placeholder="璇疯緭鍏ュ嚭鐗堢ぞ鍚嶇О"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="4" md="6" class="d-flex justify-end">
          <v-btn 
            color="primary" 
            class="text-none mr-2" 
            prepend-icon="mdi-filter-variant"
            @click="showFilterDialog = true"
          >
            绛涢€?
          </v-btn>
        </v-col>
      </v-row>

      <v-card class="elevation-2">
        <v-data-table
          :headers="headers"
          :items="tasks"
          class="elevation-0"
          :items-per-page="pageSize"
          hover
          :width="'100%'"
          :loading="loading"
          hide-default-footer
        >
          <template v-slot:top>
            <div class="d-flex align-center pa-4">
              <div class="text-caption text-medium-emphasis">
                鍏?{{ totalTasks }} 鏉¤褰?
              </div>
            </div>
          </template>

          <template v-slot:item.publisher_avatar="{ item }">
            <v-avatar size="40">
              <v-img :src="item.publisher_avatar || 'https://randomuser.me/api/portraits/lego/1.jpg'" :alt="item.publisher_username"></v-img>
            </v-avatar>
          </template>

          <template v-slot:item.task_type="{ item }">
            <v-chip
              :color="getTaskTypeColor(item.task_type)"
              size="small"
              class="status-chip"
            >
              {{ getTaskTypeName(item.task_type) }}
            </v-chip>
          </template>

          <template v-slot:item.status="{ item }">
            <v-chip
              :color="getStatusColor(item.status)"
              size="small"
              class="status-chip"
            >
              {{ getStatusName(item.status) }}
            </v-chip>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-btn
              icon
              variant="text"
              size="small"
              color="primary"
              class="mr-2"
              @click="goToTaskDetail(item)"
            >
              <v-icon>mdi-eye</v-icon>
            </v-btn>
          </template>
        </v-data-table>
        
        <div class="d-flex align-center justify-center pa-4">
          <div class="d-flex align-center">
            <span class="text-caption mr-2">姣忛〉鏄剧ず</span>
            <v-select
              v-model="pageSize"
              :items="[5, 10, 20, 50, 100]"
              density="compact"
              variant="outlined"
              hide-details
              style="width: 100px"
              @update:model-value="handlePageSizeChange"
            ></v-select>
            <span class="text-caption ml-2">鏉?/span>
          </div>
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            :total-visible="7"
            class="ml-4"
            @update:model-value="handlePageChange"
          ></v-pagination>
        </div>
      </v-card>

    <!-- 绛涢€夊璇濇 -->
    <v-dialog v-model="showFilterDialog" max-width="500">
      <v-card class="elevation-4">
        <v-card-title class="text-h6 font-weight-bold">绛涢€夋潯浠?/v-card-title>
        <v-card-text>
          <div class="d-flex flex-column gap-4">
            <v-select
              v-model="filters.status"
              :items="statusOptions"
              label="浠诲姟鐘舵€?
              clearable
              hide-details
            ></v-select>
            
            <v-select
              v-model="filters.timeRange"
              :items="timeRangeOptions"
              label="蹇€熼€夋嫨鏃堕棿鑼冨洿"
              clearable
              hide-details
              @update:model-value="handleTimeRangeChange"
            ></v-select>

            <div class="d-flex align-center gap-4">
              <v-text-field
                v-model="filters.startDate"
                label="寮€濮嬫椂闂?
                type="datetime-local"
                hide-details
                density="compact"
                :error-messages="timeError"
                @update:model-value="handleCustomTimeChange"
              ></v-text-field>
              <v-text-field
                v-model="filters.endDate"
                label="缁撴潫鏃堕棿"
                type="datetime-local"
                hide-details
                density="compact"
                :error-messages="timeError"
                @update:model-value="handleCustomTimeChange"
              ></v-text-field>
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="resetFilters">閲嶇疆</v-btn>
          <v-btn color="primary" @click="applyFilters">搴旂敤</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import reviewerApi from '@/api/reviewer'
import { useSnackbarStore } from '@/stores/snackbar'

const router = useRouter()
const snackbar = useSnackbarStore()

interface Task {
  manual_review_id: number
  manual_review_time: string
  publisher_username: string
  publisher_avatar: string
  resource_count: number
  task_type: string
  status: string
  task_type?: string
}

const headers = [
  { title: '澶村儚', key: 'publisher_avatar', align: 'center', sortable: false },
  { title: '鍑虹増绀?, key: 'publisher_username', align: 'start' },
  { title: '鏉愭枡鏁伴噺', key: 'resource_count', align: 'start' },
  { title: '鐘舵€?, key: 'status', align: 'center' },
  { title: '鎻愪氦鏃堕棿', key: 'maual_review_time', align: 'center' },
  { title: '鎿嶄綔', key: 'actions', align: 'center', sortable: false },
] as const

// 鍒嗛〉鐩稿叧
const tasks = ref<Task[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalTasks = ref(0)
const totalPages = ref(1)

// 鎼滅储鐩稿叧
const searchQuery = ref('')

// 绛涢€夌浉鍏?
const showFilterDialog = ref(false)
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
  { title: '鏈畬鎴?, value: 'undo' },
  { title: '宸插畬鎴?, value: 'completed' },
]

const timeRangeOptions = [
  { title: '鏈€杩戜竴澶?, value: '1d' },
  { title: '鏈€杩戜竴鍛?, value: '7d' },
  { title: '鏈€杩戜竴鏈?, value: '30d' },
  { title: '鏈€杩戜笁鏈?, value: '90d' },
  { title: '鏈€杩戜竴骞?, value: '365d' }
]

const getStatusColor = (status: string) => {
  switch (status) {
    case 'undo':
      return 'error'
    case 'completed':
      return 'success'
    default:
      return 'grey'
  }
}

const getStatusName = (status: string) => {
  switch (status) {
    case 'undo':
      return '鏈畬鎴?
    case 'completed':
      return '宸插畬鎴?
    default:
      return status
  }
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
      return '鍥惧儚妫€娴?
    case 'paper_text':
      return '璁烘枃妫€娴?
    case 'review_text':
      return '璇勫妫€娴?
    case 'multi_material':
      return '澶氭潗鏂欐娴?
    default:
      return taskType || '鏈煡'
  }
}

const formatTime = (timestamp: string) => {
  return timestamp // 鍚庣杩斿洖鐨勬椂闂存牸寮忓凡缁忔槸姝ｇ‘鐨勶紝鐩存帴鏄剧ず
}

const goToTaskDetail = (task: Task) => {
  router.push(`/task/detail/${task.manual_review_id}`)
}

// 鏃堕棿楠岃瘉鐩稿叧
const timeError = ref('')

// 澶勭悊蹇€熼€夋嫨鏃堕棿鑼冨洿鍙樺寲
const handleTimeRangeChange = (value: string | null) => {
  if (value) {
    filters.value.startDate = null
    filters.value.endDate = null
    timeError.value = ''
  }
}

// 澶勭悊鑷畾涔夋椂闂村彉鍖?
const handleCustomTimeChange = () => {
  filters.value.timeRange = null
  
  if (!filters.value.startDate || !filters.value.endDate) {
    timeError.value = '寮€濮嬫椂闂村拰缁撴潫鏃堕棿涓嶈兘涓虹┖'
    return
  }

  const startTime = new Date(filters.value.startDate).getTime()
  const endTime = new Date(filters.value.endDate).getTime()
  
  if (startTime >= endTime) {
    timeError.value = '寮€濮嬫椂闂村繀椤绘棭浜庣粨鏉熸椂闂?
  } else {
    timeError.value = ''
  }
}

// 閲嶇疆绛涢€夋潯浠?
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

// 搴旂敤绛涢€夋潯浠?
const applyFilters = () => {
  if (timeError.value) {
    return
  }
  
  currentPage.value = 1
  pageSize.value = 10
  fetchTasks(1, 10)
  showFilterDialog.value = false
}

// 澶勭悊鎼滅储
const handleSearch = () => {
  currentPage.value = 1
  pageSize.value = 10
  fetchTasks(1, 10)
}

// 浠庡悗绔幏鍙栦换鍔℃暟鎹?
const fetchTasks = async (page: number, pageSize: number) => {
  loading.value = true
  try {
    // 璁＄畻鏃堕棿绛涢€?
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
      query: searchQuery.value || '',
      status: filters.value.status || '',
      start_time: startTimeFilter,
      end_time: endTimeFilter
    }
    const response = await reviewerApi.getReviewerTasks(params)
    const { results: taskList, current_page, total_pages, total_users } = response.data
    
    tasks.value = taskList.map((task: any) => {
      const taskType = task.task_type || 'image'
      const resourceCount = taskType.includes('text') ? (task.text_count || 0) : (task.image_count || 0)
      return {
      manual_review_id: task.manual_review_id,
      manual_review_time: task.manual_review_time,
      publisher_username: task.publisher_username,
      publisher_avatar: 'http://122.9.45.122' + task.publisher_avatar || '',
      resource_count: resourceCount,
      task_type: taskType,
      status: task.status
      }
    })
    
    currentPage.value = current_page
    totalPages.value = total_pages
    totalTasks.value = total_users
  } catch (error) {
    console.error('鑾峰彇浠诲姟鍒楄〃澶辫触:', error)
    snackbar.showMessage('鑾峰彇浠诲姟鍒楄〃澶辫触', 'error')
  } finally {
    loading.value = false
  }
}

// 澶勭悊椤电爜鍙樺寲
const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchTasks(page, pageSize.value)
}

// 澶勭悊姣忛〉鏁伴噺鍙樺寲
const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchTasks(1, size)
}

// 鏃堕棿鏍煎紡鍖栵紝鐢ㄤ簬绛涢€夋潯浠?
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

// 鍒濆鍖?
onMounted(() => {
  fetchTasks(currentPage.value, pageSize.value)
})
</script>

<style scoped>
.v-card {
  border-radius: 12px;
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
</style>

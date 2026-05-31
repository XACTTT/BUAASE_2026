<template>
  <v-container>
    <!-- 欢迎卡片 -->
    <v-card class="mb-6">
      <v-card-title class="text-h5">
        欢迎使用学术诚信检测系统
      </v-card-title>
      <v-card-text>
        <p>这里是系统的主页，您可以：</p>
        <v-list>
          <v-list-item v-if="userStore.role === 'publisher'">
            <v-list-item-title>
              <v-icon start>mdi-file-upload</v-icon>
              上传文件进行检测
            </v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>
              <v-icon start>mdi-history</v-icon>
              查看历史检测记录
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <!-- 资源列表 -->
    <v-card v-if="userStore.role !== 'reviewer'">
      <v-card-title class="d-flex align-center">
        <h2 class="text-h6 font-weight-bold">我的资源</h2>
        <v-spacer></v-spacer>
        <v-btn variant="text" size="small" @click="fetchResources" :loading="loading">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text v-if="loading" class="d-flex justify-center py-8">
        <v-progress-circular indeterminate color="primary" />
      </v-card-text>

      <v-card-text v-else-if="resources.length === 0" class="text-center py-8">
        <v-icon size="48" color="grey" class="mb-2">mdi-folder-open</v-icon>
        <div class="text-body-2 text-grey">{{ userStore.role === 'publisher' ? '暂无资源，请先上传文件' : '暂无资源' }}</div>
      </v-card-text>

      <v-data-table v-else :headers="headers" :items="resources" :items-per-page="10" hide-default-footer>
        <template v-slot:item.title="{ item }">
          <span class="text-body-2 font-weight-medium">{{ item.title || '-' }}</span>
        </template>

        <template v-slot:item.container_type="{ item }">
          <v-chip size="small" :color="getContainerTypeColor(item.container_type)" variant="tonal">
            {{ getContainerTypeLabel(item.container_type) }}
          </v-chip>
        </template>

        <template v-slot:item.file_names="{ item }">
          <div v-if="item.file_names && item.file_names.length" class="d-flex flex-wrap ga-1">
            <v-chip v-for="(name, idx) in item.file_names.slice(0, 2)" :key="idx" size="x-small" variant="outlined">
              {{ name }}
            </v-chip>
            <v-chip v-if="item.file_names.length > 2" size="x-small" variant="outlined" color="grey">
              +{{ item.file_names.length - 2 }}
            </v-chip>
          </div>
          <span v-else class="text-grey text-caption">-</span>
        </template>

        <template v-slot:item.tag="{ item }">
          <span class="text-body-2">{{ getSubjectLabel(item.tag) }}</span>
        </template>

        <template v-slot:item.detection_task_status="{ item }">
          <v-chip v-if="item.detection_task_id" :color="getStatusColor(item.detection_task_status)" size="small">
            {{ getStatusLabel(item.detection_task_status) }}
          </v-chip>
          <span v-else class="text-grey text-caption">未检测</span>
        </template>

        <template v-slot:item.created_at="{ item }">
          <span class="text-body-2">{{ formatDateTime(item.created_at) }}</span>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            size="small"
            color="primary"
            variant="tonal"
            :disabled="!item.detection_task_id || !canViewResult(item.detection_task_status)"
            @click="handleViewResult(item)"
          >
            查看结果
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSnackbarStore } from '@/stores/snackbar'
import { useUserStore } from '@/stores/user'
import publisher from '@/api/publisher'

const router = useRouter()
const snackbar = useSnackbarStore()
const userStore = useUserStore()

interface ResourceContainer {
  id: number
  title: string
  container_type: string
  file_names: string[]
  tag: string
  detection_task_id: number | null
  detection_task_status: string | null
  task_type: string | null
  task_name: string | null
  created_at: string
}

const resources = ref<ResourceContainer[]>([])
const loading = ref(false)

const headers = [
  { title: '名称', key: 'title', align: 'center' as const, width: '140px' },
  { title: '类型', key: 'container_type', align: 'center' as const, width: '110px' },
  { title: '文件', key: 'file_names', align: 'start' as const, width: '180px' },
  { title: '学科', key: 'tag', align: 'center' as const, width: '100px' },
  { title: '检测状态', key: 'detection_task_status', align: 'center' as const, width: '120px' },
  { title: '创建时间', key: 'created_at', align: 'center' as const, width: '160px' },
  { title: '操作', key: 'actions', sortable: false, align: 'center' as const, width: '120px' }
]

const fetchResources = async () => {
  loading.value = true
  try {
    const { data } = await publisher.getResourceContainers()
    resources.value = Array.isArray(data) ? data : []
  } catch {
    snackbar.showMessage('获取资源列表失败', 'error')
  } finally {
    loading.value = false
  }
}

const canViewResult = (status: string | null) => {
  if (!status) return false
  return ['completed', 'partially_completed', 'failed'].includes(status)
}

const handleViewResult = (item: ResourceContainer) => {
  if (!item.detection_task_id) return
  const type = item.task_type || ''
  const query = type ? `?type=${type}` : ''
  router.push(`/step/${item.detection_task_id}${query}`)
}

const getContainerTypeLabel = (type: string) => {
  const map: Record<string, string> = {
    image: '图片',
    paper: '论文',
    review: 'Review',
    multi_material: '综合',
  }
  return map[type] || type || '-'
}

const getContainerTypeColor = (type: string) => {
  const map: Record<string, string> = {
    image: 'primary',
    paper: 'success',
    review: 'warning',
    multi_material: 'purple',
  }
  return map[type] || 'grey'
}

const getSubjectLabel = (subject?: string) => {
  const map: Record<string, string> = {
    computer_science: '计算机科学',
    artificial_intelligence: '人工智能',
    mathematics: '数学',
    physics: '物理',
    chemistry: '化学',
    biology: '生物',
    medicine: '医学',
    engineering: '工程',
    graphics: '图形学',
    other: '其他'
  }
  return subject ? (map[subject] || subject) : '-'
}

const getStatusLabel = (status: string | null) => {
  const map: Record<string, string> = {
    pending: '排队中',
    in_progress: '进行中',
    analyzing: '分析中',
    completed: '已完成',
    partially_completed: '部分完成',
    failed: '失败',
  }
  return status ? (map[status] || status) : '未检测'
}

const getStatusColor = (status: string | null) => {
  const map: Record<string, string> = {
    pending: 'yellow',
    in_progress: 'info',
    analyzing: 'warning',
    completed: 'success',
    partially_completed: 'warning',
    failed: 'error',
  }
  return status ? (map[status] || 'grey') : 'grey'
}

const formatDateTime = (dateTime: string) => {
  if (!dateTime) return ''
  const date = new Date(dateTime)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

onMounted(() => {
  fetchResources()
})
</script>

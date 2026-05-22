<template>
  <v-card flat border="0">
    <!-- Loading -->
    <v-card-text v-if="loading" class="pa-0 mt-4">
      <div class="d-flex justify-center align-center" style="min-height: 400px">
        <v-progress-circular indeterminate color="primary" size="64" />
      </div>
    </v-card-text>

    <!-- Error / no data -->
    <v-card-text v-else-if="error" class="pa-0 mt-4">
      <div class="d-flex flex-column justify-center align-center" style="min-height: 400px">
        <v-icon size="64" color="error" class="mb-4">mdi-alert-circle</v-icon>
        <div class="text-h6 mb-2">加载失败</div>
        <div class="text-body-2 text-medium-emphasis">{{ error }}</div>
        <v-btn color="primary" class="mt-4" @click="fetchData">重试</v-btn>
      </div>
    </v-card-text>

    <!-- Image detection -->
    <DetectionReviewStep v-else-if="isImageTask" :task_id="taskId" />

    <!-- Text detection (paper_text, review_text, multi_material) -->
    <TextDetectionResultView v-else :task-id="taskId" :task-meta="taskMeta" />
  </v-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { RouteParams } from 'vue-router'
import DetectionReviewStep from '@/components/steps/DetectionReviewStep.vue'
import TextDetectionResultView from '@/components/steps/TextDetectionResultView.vue'
import { useSnackbarStore } from '@/stores/snackbar'
import publisher from '@/api/publisher'

const router = useRouter()
const route = useRoute()
const snackbar = useSnackbarStore()

const taskId = computed(() => (route.params as RouteParams & { id: string }).id)
const loading = ref(true)
const error = ref('')
const taskMeta = ref<any>(null)

const resolvedTaskType = computed(() => {
  return taskMeta.value?.task_type || taskMeta.value?.detect_type || ''
})

const isImageTask = computed(() => {
  const t = resolvedTaskType.value
  return t === 'image' || t === 'Image'
})

const fetchData = async () => {
  loading.value = true
  error.value = ''
  try {
    // Permission check
    const accessResp = (await publisher.ifHasPermission({ task_id: taskId.value })).data.access
    if (accessResp !== true) {
      router.push('/404')
      return
    }
    // Fetch task data
    taskMeta.value = (await publisher.getStructuredTaskResult(taskId.value)).data
    if (!taskMeta.value?.detect_type && taskMeta.value?.task_type === 'image') {
      taskMeta.value.detect_type = 'image'
    }
  } catch (err) {
    error.value = '获取任务详情失败'
    snackbar.showMessage('获取任务详情失败', 'error')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.v-card {
  box-shadow: none;
}
</style>

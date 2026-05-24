<template>
  <v-card flat border="0">
    <v-card-text v-if="loading" class="pa-0 mt-4">
      <div class="d-flex justify-center align-center" style="min-height: 400px">
        <v-progress-circular indeterminate color="primary" size="64" />
      </div>
    </v-card-text>

    <v-card-text v-else-if="error" class="pa-0 mt-4">
      <div class="d-flex flex-column justify-center align-center" style="min-height: 400px">
        <v-icon size="64" color="error" class="mb-4">mdi-alert-circle</v-icon>
        <div class="text-h6 mb-2">加载失败</div>
        <div class="text-body-2 text-medium-emphasis">{{ error }}</div>
        <v-btn color="primary" class="mt-4" @click="fetchData">重试</v-btn>
      </div>
    </v-card-text>

    <DetectionReviewStep v-else-if="isImageTask" :task_id="taskId" />

    <MultiMaterialResultView
      v-else-if="isMultiMaterialTask"
      :task-id="taskId"
      :task-meta="taskMeta"
    />

    <TextDetectionResultView
      v-else
      :task-id="taskId"
      :task-meta="taskMeta"
    />
  </v-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { RouteParams } from 'vue-router'
import DetectionReviewStep from '@/components/steps/DetectionReviewStep.vue'
import TextDetectionResultView from '@/components/steps/TextDetectionResultView.vue'
import MultiMaterialResultView from '@/components/steps/MultiMaterialResultView.vue'
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
  const type = resolvedTaskType.value
  return type === 'image' || type === 'Image'
})

const isMultiMaterialTask = computed(() => {
  const type = resolvedTaskType.value
  return type === 'multi_material' || type === 'multi'
})

const fetchData = async () => {
  loading.value = true
  error.value = ''

  try {
    const accessResp = await publisher.ifHasPermission({ task_id: taskId.value })
    if (accessResp.data?.access !== true) {
      router.push('/404')
      return
    }

    const detailResp = await publisher.getStructuredTaskResult(taskId.value)
    taskMeta.value = detailResp.data

    if (!taskMeta.value?.detect_type && taskMeta.value?.task_type === 'image') {
      taskMeta.value.detect_type = 'image'
    }
  } catch (err) {
    error.value = '获取任务详情失败'
    snackbar.showMessage(error.value, 'error')
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.v-card {
  box-shadow: none;
}
</style>

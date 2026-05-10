<template>
  <v-card flat border="0">
    <v-card-text class="pa-0 mt-4">
      <template v-if="loading">
        <div class="pa-8 text-center text-medium-emphasis">加载中...</div>
      </template>
      <template v-else-if="taskMeta?.detect_type === 'image'">
        <DetectionReviewStep :task_id="taskId" />
      </template>
      <template v-else>
        <v-container class="py-8">
          <v-row>
            <v-col cols="12">
              <v-card class="mb-6" elevation="2" rounded="lg">
                <v-card-title class="text-h6">任务概览</v-card-title>
                <v-card-text>
                  <div class="mb-2">任务编号：{{ taskId }}</div>
                  <div class="mb-2">任务类型：{{ formatDetectType(taskMeta?.detect_type) }}</div>
                  <div class="mb-2">状态：{{ formatStatus(taskMeta?.status) }}</div>
                  <div v-if="taskMeta?.summary" class="mb-2">摘要：{{ taskMeta.summary }}</div>
                  <div v-if="taskMeta?.confidence_score !== null && taskMeta?.confidence_score !== undefined" class="mb-2">
                    置信度：{{ Number(taskMeta.confidence_score).toFixed(4) }}
                  </div>
                  <div v-if="taskMeta?.overall_is_fake !== null && taskMeta?.overall_is_fake !== undefined" class="mb-2">
                    判定结果：{{ taskMeta.overall_is_fake ? '疑似异常' : '未见明显异常' }}
                  </div>
                  <div v-if="taskMeta?.failure_reason" class="error-text">
                    失败原因：{{ taskMeta.failure_reason }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" v-if="dimensions.length">
              <v-card class="mb-6" elevation="2" rounded="lg">
                <v-card-title class="text-h6">检测维度</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col v-for="dimension in dimensions" :key="dimension.name" cols="12" md="6">
                      <v-card variant="outlined">
                        <v-card-title class="text-subtitle-1">{{ dimension.name }}</v-card-title>
                        <v-card-text>
                          <div class="mb-2">分数：{{ formatMaybeNumber(dimension.score) }}</div>
                          <div v-if="dimension.summary">{{ dimension.summary }}</div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" v-if="evidenceText">
              <v-card elevation="2" rounded="lg">
                <v-card-title class="text-h6">证据明细</v-card-title>
                <v-card-text>
                  <pre class="structured-pre">{{ evidenceText }}</pre>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </template>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
//注意鉴权！！！
import { computed, onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { RouteParams } from 'vue-router'
import DetectionReviewStep from '@/components/steps/DetectionReviewStep.vue'
import { useSnackbarStore } from '@/stores/snackbar';
import publisher from '@/api/publisher'
const snackbar = useSnackbarStore();

const router = useRouter()
const route = useRoute()

// 获取任务ID
const taskId = computed(() => (route.params as RouteParams & { id: string }).id)
const loading = ref(true)
const taskMeta = ref<any>(null)
const dimensions = computed(() => Array.isArray(taskMeta.value?.result?.dimensions) ? taskMeta.value.result.dimensions : [])
const evidenceText = computed(() => {
  const evidence = taskMeta.value?.result?.evidence
  if (!evidence || typeof evidence !== 'object') {
    return ''
  }
  return JSON.stringify(evidence, null, 2)
})

const formatDetectType = (value?: string) => {
  switch (value) {
    case 'paper':
      return '论文检测'
    case 'review':
      return 'Review检测'
    case 'multi':
      return '多材料综合检测'
    case 'image':
      return '图片检测'
    default:
      return value || '未知'
  }
}

const formatStatus = (value?: string) => {
  switch (value) {
    case 'pending':
      return '排队中'
    case 'in_progress':
      return '进行中'
    case 'completed':
      return '已完成'
    case 'failed':
      return '失败'
    default:
      return value || '未知'
  }
}

const formatMaybeNumber = (value: unknown) => {
  const num = Number(value)
  return Number.isFinite(num) ? num.toFixed(4) : String(value ?? '')
}

// 组件挂载时获取任务数据
onMounted(async () => {
  try {
    const accessResp = (await publisher.ifHasPermission({task_id: taskId.value})).data.access
    if (accessResp !== true) {
      router.push('/404')
      return
    }
    taskMeta.value = (await publisher.getStructuredTaskResult(taskId.value)).data
  } catch (error) {
    snackbar.showMessage('获取任务详情失败', 'error')
    router.push('/history')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.v-card {
  box-shadow: none;
}

.structured-pre {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
</style>

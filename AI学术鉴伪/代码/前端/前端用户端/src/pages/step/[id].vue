<template>
  <v-card flat border="0">
    <v-card-text class="pa-0 mt-4">
      <template v-if="loading">
        <div class="pa-8 text-center text-medium-emphasis">加载中...</div>
      </template>
      <template v-else-if="useSample && resolvedTaskType === 'image'">
        <ImageDetectionReview :task_id="taskId" :task_type="resolvedTaskType" />
      </template>
      <template v-else-if="useSample && resolvedTaskType === 'paper_text'">
        <PaperTextDetectionReview :task_id="taskId" :task_type="resolvedTaskType" />
      </template>
      <template v-else-if="useSample && resolvedTaskType === 'review_text'">
        <ReviewTextDetectionReview :task_id="taskId" :task_type="resolvedTaskType" />
      </template>
      <template v-else-if="isImageTask">
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
                  <div v-if="taskMeta?.task_name" class="mb-2">任务名称：{{ taskMeta.task_name }}</div>
                  <div class="mb-2">任务类型：{{ formatTaskType(resolvedTaskType) }}</div>
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

            <v-col cols="12" v-if="materialSummary">
              <v-card class="mb-6" elevation="2" rounded="lg">
                <v-card-title class="text-h6">材料统计</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col
                      v-for="item in materialSummaryItems"
                      :key="item.label"
                      cols="12"
                      md="4"
                    >
                      <v-card variant="outlined">
                        <v-card-text class="text-center">
                          <div class="text-h5 font-weight-bold">{{ item.value }}</div>
                          <div class="text-medium-emphasis">{{ item.label }}</div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" v-if="isTextTask && textResults.length">
              <v-card class="mb-6" elevation="2" rounded="lg">
                <v-card-title class="text-h6">文本检测结果</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col
                      v-for="item in textResults"
                      :key="item.result_id"
                      cols="12"
                      md="6"
                    >
                      <v-card variant="outlined">
                        <v-card-text>
                          <div class="mb-2">资源编号：{{ item.resource_id }}</div>
                          <div class="mb-2">文本类型：{{ item.text_type || '-' }}</div>
                          <div class="mb-2">状态：{{ formatStatus(item.status) }}</div>
                          <div v-if="item.confidence_score !== null && item.confidence_score !== undefined" class="mb-2">
                            置信度：{{ Number(item.confidence_score).toFixed(4) }}
                          </div>
                          <div v-if="item.is_fake !== null && item.is_fake !== undefined">
                            判定结果：{{ item.is_fake ? '疑似异常' : '未见明显异常' }}
                          </div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
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

            <v-col cols="12" v-if="llmAnalysis">
              <v-card elevation="2" rounded="lg" class="mb-6">
                <v-card-title class="text-h6">
                  大模型综合分析
                  <v-chip size="small" class="ml-2" :color="llmAnalysis.risk_level === 'high' ? 'error' : llmAnalysis.risk_level === 'medium' ? 'warning' : 'success'">
                    {{ llmAnalysis.risk_level || '未知' }}
                  </v-chip>
                </v-card-title>
                <v-card-text>
                  <v-row v-if="llmAnalysisItems.length">
                    <v-col
                      v-for="item in llmAnalysisItems"
                      :key="item.label"
                      cols="12"
                      :md="item.isArray ? 12 : 6"
                    >
                      <v-card variant="outlined" class="mb-2">
                        <v-card-text>
                          <div class="text-caption text-medium-emphasis mb-1">{{ item.label }}</div>
                          <template v-if="item.isArray">
                            <ul class="pl-4 mb-0">
                              <li v-for="(entry, idx) in item.value" :key="idx">{{ entry }}</li>
                            </ul>
                          </template>
                          <template v-else>
                            <div>{{ item.value }}</div>
                          </template>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                  <pre v-else class="structured-pre">{{ llmAnalysisRaw }}</pre>
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
import ImageDetectionReview from '@/components/reviews/ImageDetectionReview.vue'
import PaperTextDetectionReview from '@/components/reviews/PaperTextDetectionReview.vue'
import ReviewTextDetectionReview from '@/components/reviews/ReviewTextDetectionReview.vue'
import { useSnackbarStore } from '@/stores/snackbar'
import publisher from '@/api/publisher'
const snackbar = useSnackbarStore()

const router = useRouter()
const route = useRoute()

// 获取任务ID
const taskId = computed(() => (route.params as RouteParams & { id: string }).id)
const useSample = computed(() => route.query.sample === '1')
const loading = ref(true)
const taskMeta = ref<any>(null)
const resolvedTaskType = computed(() => {
  return taskMeta.value?.task_type || (route.query.type as string) || taskMeta.value?.detect_type || 'image'
})
const isTextTask = computed(() => ['paper_text', 'review_text'].includes(resolvedTaskType.value))
const isImageTask = computed(() => {
  if (isTextTask.value) {
    return false
  }
  if (resolvedTaskType.value === 'image') {
    return true
  }
  return taskMeta.value?.detect_type === 'image'
})
const materialSummary = computed(() => {
  const summary = taskMeta.value?.material_summary || taskMeta.value?.result?.material_summary
  return summary && typeof summary === 'object' ? summary : null
})
const materialSummaryItems = computed(() => {
  const summary = materialSummary.value
  if (!summary) {
    return []
  }

  const labelMap: Record<string, string> = {
    paper_file_count: '论文文件数',
    image_count: '图片总数',
    review_file_count: '评审文件数',
    review_text_count: '评审文本数',
    text_count: '文本总数',
    completed_count: '已完成',
    fake_count: '疑似异常',
  }

  return Object.entries(summary).map(([key, value]) => ({
    label: labelMap[key] || key,
    value,
  }))
})
const textResults = computed(() => Array.isArray(taskMeta.value?.results) ? taskMeta.value.results : [])
const dimensions = computed(() => Array.isArray(taskMeta.value?.result?.dimensions) ? taskMeta.value.result.dimensions : [])
const evidenceText = computed(() => {
  const evidence = taskMeta.value?.result?.evidence
  if (!evidence || typeof evidence !== 'object') {
    return ''
  }
  try {
    const text = JSON.stringify(evidence, null, 2)
    return text.length > 50000 ? text.slice(0, 50000) + '\n... [已截断，完整数据见后端]' : text
  } catch {
    return '[证据数据无法序列化]'
  }
})

const llmAnalysis = computed(() => {
  return taskMeta.value?.result?.llm_analysis ?? null
})

const llmAnalysisRaw = computed(() => {
  const analysis = llmAnalysis.value
  if (!analysis) return ''
  try {
    return JSON.stringify(analysis, null, 2)
  } catch {
    return String(analysis)
  }
})

const llmAnalysisItems = computed(() => {
  const analysis = llmAnalysis.value
  if (!analysis || typeof analysis !== 'object') return []
  const labelMap: Record<string, string> = {
    summary: '综合摘要',
    risk_level: '风险等级',
    confidence: '置信度',
    recommendations: '建议',
    evidence: '证据',
    suspicious_patterns: '可疑模式',
    signals: '信号指标',
    consistency_issues: '一致性问题',
    raw_text: '原始输出',
  }
  return Object.entries(analysis)
    .filter(([, v]) => v !== null && v !== undefined)
    .map(([key, value]) => ({
      label: labelMap[key] || key,
      value,
      isArray: Array.isArray(value),
    }))
})

const formatTaskType = (value?: string) => {
  switch (value) {
    case 'paper':
      return '论文材料检测'
    case 'review':
      return 'Review材料检测'
    case 'multi':
      return '多材料综合检测'
    case 'image':
      return '图片检测'
    case 'paper_text':
      return '论文文本检测'
    case 'review_text':
      return 'Review文本检测'
    case 'multi_material':
      return '综合检测'
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
    case 'analyzing':
      return '大模型分析中'
    case 'completed':
      return '已完成'
    case 'partially_completed':
      return '部分完成'
    case 'failed':
      return '失败'
    default:
      return value || '未知'
  }
}

const formatMaybeNumber = (value: unknown) => {
  if (value === null || value === undefined) return ''
  const num = Number(value)
  return Number.isFinite(num) ? num.toFixed(4) : String(value)
}

// 组件挂载时获取任务数据
onMounted(async () => {
  if (useSample.value) {
    taskMeta.value = {
      task_type: (route.query.type as string) || 'image',
      detect_type: (route.query.type as string) === 'image' ? 'image' : undefined,
    }
    loading.value = false
    return
  }
  try {
    const accessResp = (await publisher.ifHasPermission({task_id: taskId.value})).data.access
    if (accessResp !== true) {
      router.push('/404')
      return
    }
    taskMeta.value = (await publisher.getStructuredTaskResult(taskId.value)).data
    if (!taskMeta.value?.detect_type && taskMeta.value?.task_type === 'image') {
      taskMeta.value.detect_type = 'image'
    }
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

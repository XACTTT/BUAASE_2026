<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTheme } from 'vuetify'
import { useSnackbarStore } from '@/stores/snackbar'
import { useUserStore } from '@/stores/user'
import publisher from '@/api/publisher'
import { useRouter } from 'vue-router'

interface Props {
  taskId: string
  taskMeta: any
}

const props = defineProps<Props>()
const router = useRouter()
const snackbar = useSnackbarStore()
const theme = useTheme()
const userStore = useUserStore()

const isDarkMode = computed(() => theme.global.current.value.dark)
const apiBaseUrl = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')

const loading = ref(true)

// --- Data ---
interface TextResultItem {
  result_id: string
  resource_id: number
  text_type: string
  status: string
  is_fake: boolean
  confidence_score: number
  detection_time: string
}

interface ParagraphInfo {
  paragraph_index: number
  text: string
  ai_probability: number
  reason: string
}

interface TextDetail {
  resource_id: number
  status: string
  is_fake: boolean
  confidence_score: number
  ai_generated_paragraphs: ParagraphInfo[]
  factual_fake_reason: string
  template_tendency_score: number
  template_analysis_reason: string
  detection_time: string
}

interface Reviewer {
  id: number
  username: string
  avatar: string
}

const textList = ref<TextResultItem[]>([])
const textDetails = ref<Map<number, TextDetail>>(new Map())
const allReviewers = ref<Reviewer[]>([])

// --- Review dialog state ---
const showReviewDialog = ref(false)
const selectedReviewers = ref<number[]>([])
const reviewReason = ref('')
const selectedTextIds = ref<number[]>([])
const reviewSearchQuery = ref('')
const submittingReview = ref(false)

// --- Paragraph detail dialog ---
const showParagraphDialog = ref(false)
const selectedParagraph = ref<ParagraphInfo | null>(null)

// --- Computed ---
const taskType = computed(() => {
  return props.taskMeta?.task_type || props.taskMeta?.detect_type || ''
})

const hasPaperResults = computed(() => {
  return textList.value.some(item => item.text_type === 'paper_text')
})

const hasReviewResults = computed(() => {
  return textList.value.some(item => item.text_type === 'review_text')
})

const paperResults = computed(() => {
  return textList.value.filter(item => item.text_type === 'paper_text')
})

const reviewResults = computed(() => {
  return textList.value.filter(item => item.text_type === 'review_text')
})

const firstDetectionTime = computed(() => {
  if (textList.value.length === 0) return ''
  const times = textList.value.map(r => r.detection_time).filter(Boolean)
  if (times.length === 0) return ''
  return times.sort()[0]
})

// Overall conclusion from taskMeta
const overallConclusion = computed(() => {
  if (props.taskMeta?.overall_is_fake !== undefined && props.taskMeta?.confidence_score !== undefined) {
    const isFake = props.taskMeta.overall_is_fake
    const score = props.taskMeta.confidence_score
    return {
      isFake,
      confidence: (score * 100).toFixed(1) + '%',
      color: isFake ? 'error' : 'success',
      label: isFake ? '检测到AI生成内容' : '未检测到AI生成内容'
    }
  }
  return null
})

// --- Paper text statistics (aggregated across all paper results) ---
const paperStatistics = computed(() => {
  let total = 0
  let high = 0
  let medium = 0
  let low = 0

  for (const item of paperResults.value) {
    const detail = textDetails.value.get(item.resource_id)
    if (detail && detail.ai_generated_paragraphs) {
      for (const para of detail.ai_generated_paragraphs) {
        total++
        if (para.ai_probability > 0.8) high++
        else if (para.ai_probability > 0.5) medium++
        else low++
      }
    }
  }

  return { total, high, medium, low }
})

// All paragraphs across paper results
const allPaperParagraphs = computed(() => {
  const paragraphs: (ParagraphInfo & { resource_id: number })[] = []
  for (const item of paperResults.value) {
    const detail = textDetails.value.get(item.resource_id)
    if (detail && detail.ai_generated_paragraphs) {
      for (const para of detail.ai_generated_paragraphs) {
        paragraphs.push({ ...para, resource_id: item.resource_id })
      }
    }
  }
  return paragraphs
})

// Top 5 high risk paragraphs
const topRiskParagraphs = computed(() => {
  return [...allPaperParagraphs.value]
    .sort((a, b) => b.ai_probability - a.ai_probability)
    .slice(0, 5)
})

// Aggregated factual fake reason
const factualFakeReasons = computed(() => {
  const reasons: string[] = []
  for (const item of paperResults.value) {
    const detail = textDetails.value.get(item.resource_id)
    if (detail && detail.factual_fake_reason) {
      reasons.push(detail.factual_fake_reason)
    }
  }
  return reasons
})

// Review text: aggregated template data
const reviewTemplateData = computed(() => {
  const data: { score: number; reason: string; resource_id: number }[] = []
  for (const item of reviewResults.value) {
    const detail = textDetails.value.get(item.resource_id)
    if (detail && detail.template_tendency_score !== undefined) {
      data.push({
        score: detail.template_tendency_score,
        reason: detail.template_analysis_reason || '',
        resource_id: item.resource_id
      })
    }
  }
  return data
})

// Average template tendency score
const avgTemplateScore = computed(() => {
  if (reviewTemplateData.value.length === 0) return 0
  const sum = reviewTemplateData.value.reduce((acc, d) => acc + d.score, 0)
  return sum / reviewTemplateData.value.length
})

const templateLevel = computed(() => {
  const score = avgTemplateScore.value
  if (score > 0.7) return { level: '高度模板化', color: 'error', icon: 'mdi-alert-octagon' }
  if (score > 0.4) return { level: '中度模板化', color: 'warning', icon: 'mdi-alert' }
  return { level: '低度模板化', color: 'success', icon: 'mdi-check-circle' }
})

// LLM analysis
const llmAnalysis = computed(() => {
  return props.taskMeta?.result?.llm_analysis || props.taskMeta?.ai_response?.llm_analysis || null
})

// Dimensions
const dimensions = computed(() => {
  return props.taskMeta?.result?.dimensions || null
})

// Evidence
const evidence = computed(() => {
  return props.taskMeta?.result?.evidence || null
})

// Review submission
const canSubmitReview = computed(() => {
  return selectedTextIds.value.length > 0 && selectedReviewers.value.length > 0
})

const filteredReviewers = computed(() => {
  if (!reviewSearchQuery.value) return allReviewers.value
  const q = reviewSearchQuery.value.toLowerCase()
  return allReviewers.value.filter(r => r.username.toLowerCase().includes(q))
})

// --- Helpers ---
function getProbabilityColor(probability: number): string {
  if (probability > 0.8) return 'error'
  if (probability > 0.5) return 'warning'
  return 'success'
}

function getProbabilityLevel(probability: number): string {
  if (probability > 0.8) return '高风险'
  if (probability > 0.5) return '中风险'
  return '低风险'
}

function getProbabilityClass(probability: number): string {
  if (probability > 0.8) return 'high-probability'
  if (probability > 0.5) return 'medium-probability'
  return 'low-probability'
}

function getImageUrl(url: string): string {
  if (!url) return ''
  if (/^https?:\/\//.test(url)) return url
  return `${apiBaseUrl}${url}`
}

function formatDateTime(dateTime: string): string {
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

function showParagraphDetail(paragraph: ParagraphInfo) {
  selectedParagraph.value = paragraph
  showParagraphDialog.value = true
}

function openReviewDialog() {
  selectedTextIds.value = textList.value.map(item => item.resource_id)
  selectedReviewers.value = []
  reviewReason.value = ''
  showReviewDialog.value = true
}

function toggleTextId(resourceId: number) {
  const idx = selectedTextIds.value.indexOf(resourceId)
  if (idx >= 0) {
    selectedTextIds.value.splice(idx, 1)
  } else {
    selectedTextIds.value.push(resourceId)
  }
}

function getTemplateSuggestion(score: number): string {
  if (score > 0.7) {
    return '建议：该评审意见模板化倾向严重，建议审稿人重新审视并提供更具针对性的专业意见。'
  } else if (score > 0.4) {
    return '建议：该评审意见存在一定模板化痕迹，建议审稿人结合论文具体内容补充更多细节分析。'
  } else {
    return '建议：该评审意见个性化程度较高，展现了独立的学术判断，质量较好。'
  }
}

// Chinese label map for LLM analysis
function getChineseLabel(key: string): string {
  const map: Record<string, string> = {
    risk_level: '风险等级',
    risk_score: '风险评分',
    summary: '总结',
    analysis: '分析',
    conclusion: '结论',
    recommendation: '建议',
    confidence: '置信度',
    findings: '发现',
    evidence: '证据',
    method: '方法',
    details: '详情',
    ai_probability: 'AI概率',
    fake_probability: '造假概率',
    template_score: '模板化评分',
    overall_assessment: '总体评估',
    key_findings: '关键发现',
    suggestions: '改进建议',
    risk_factors: '风险因素'
  }
  return map[key] || key
}

function formatLlmAnalysisValue(value: unknown): string {
  if (value === null || value === undefined) return ''
  if (typeof value === 'string') return value
  if (typeof value === 'number') return String(value)
  if (typeof value === 'boolean') return value ? '是' : '否'
  try {
    return JSON.stringify(value, null, 2)
  } catch {
    return String(value)
  }
}

// --- API actions ---
const downloadReport = async () => {
  try {
    const response = await publisher.downloadReport(props.taskId)
    const contentDisposition = response.headers['content-disposition']
    let fileName = `task_${props.taskId}_report.pdf`
    if (contentDisposition) {
      const match = contentDisposition.match(/filename="(.+)"/)
      if (match) fileName = match[1]
    }
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = fileName
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    snackbar.showMessage('报告下载失败', 'error')
  }
}

const submitReview = async () => {
  if (!canSubmitReview.value) return
  submittingReview.value = true
  try {
    await publisher.dispatchAnnual({
      text_ids: selectedTextIds.value,
      reviewers: selectedReviewers.value,
      reason: reviewReason.value
    })
    snackbar.showMessage('已提交人工审核任务，请等待审核', 'success')
    showReviewDialog.value = false
    router.push('/annual')
  } catch (error: any) {
    let message = '提交人工审核任务失败'
    if (error?.code === 'ERR_NETWORK') {
      message = '用户无权限'
    }
    snackbar.showMessage(message, 'error')
  } finally {
    submittingReview.value = false
  }
}

// --- Data loading ---
onMounted(async () => {
  loading.value = true
  try {
    // Fetch text results list
    const textListResp = await publisher.getTaskTextResults(props.taskId)
    const results = textListResp.data?.results || []
    textList.value = results

    // Fetch detail for each result
    const detailPromises = results.map(async (item: TextResultItem) => {
      try {
        const detailResp = await publisher.getSingleTextResult(item.resource_id)
        textDetails.value.set(item.resource_id, detailResp.data)
      } catch (err) {
        console.error(`获取文本资源 ${item.resource_id} 详情失败:`, err)
      }
    })
    await Promise.all(detailPromises)

    // Fetch reviewers
    try {
      const resp = await publisher.getReviewers({ publisher_id: userStore.id })
      allReviewers.value = Array.isArray(resp.data?.reviewers) ? resp.data.reviewers : []
    } catch (err) {
      console.error('获取审核人员失败:', err)
      allReviewers.value = []
    }
  } catch (error) {
    console.error('获取文本检测结果失败:', error)
    snackbar.showMessage('获取文本检测结果失败', 'error')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <!-- Loading state -->
  <v-container class="mt-8" v-if="loading">
    <v-row justify="center" align="center" style="min-height: 300px">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary" size="64" class="mb-4" />
        <div class="text-h6 text-grey">正在加载检测结果...</div>
      </v-col>
    </v-row>
  </v-container>

  <!-- Main content -->
  <v-container class="mt-8" v-else>
    <!-- ========== Top Info Card ========== -->
    <v-row>
      <v-col cols="12">
        <v-card class="mb-8 pa-6" elevation="2" rounded="lg">
          <v-row>
            <!-- Left: progress ring or overall conclusion -->
            <v-col cols="4" class="border-r">
              <div class="detection-summary">
                <v-progress-circular
                  v-if="overallConclusion"
                  :model-value="parseFloat(overallConclusion.confidence)"
                  :size="160"
                  :width="12"
                  :color="overallConclusion.color"
                  class="custom-progress"
                >
                  <div class="progress-content">
                    <div class="text-h4 font-weight-bold responsive-text">{{ overallConclusion.confidence }}</div>
                    <div class="text-subtitle-2 mt-1 responsive-text">
                      {{ overallConclusion.isFake ? 'AI生成概率' : '可信度' }}
                    </div>
                  </div>
                </v-progress-circular>
                <v-progress-circular
                  v-else
                  :model-value="100"
                  :size="160"
                  :width="12"
                  color="primary"
                  class="custom-progress"
                >
                  <div class="progress-content">
                    <div class="text-h4 font-weight-bold responsive-text">{{ textList.length }}</div>
                    <div class="text-subtitle-2 mt-1 responsive-text">检测结果数</div>
                  </div>
                </v-progress-circular>
              </div>
            </v-col>

            <!-- Right: info and buttons -->
            <v-col cols="8" class="pl-8">
              <div class="d-flex flex-column justify-space-between h-100">
                <!-- Task info -->
                <div class="task-info mb-8">
                  <div class="text-h6 mb-4">任务信息</div>
                  <div class="d-flex flex-column gap-2">
                    <div class="info-item d-flex align-center" :class="isDarkMode ? 'info-item-dark' : ''">
                      <v-icon :color="isDarkMode ? 'grey-lighten-1' : 'grey-darken-2'" class="mr-2">mdi-clock-outline</v-icon>
                      <span class="text-body-1">检测时间：{{ formatDateTime(firstDetectionTime) }}</span>
                    </div>
                    <div class="info-item d-flex align-center" :class="isDarkMode ? 'info-item-dark' : ''">
                      <v-icon :color="isDarkMode ? 'grey-lighten-1' : 'grey-darken-2'" class="mr-2">mdi-pound</v-icon>
                      <span class="text-body-1">任务编号：{{ taskId }}</span>
                    </div>
                    <div v-if="overallConclusion" class="info-item d-flex align-center" :class="isDarkMode ? 'info-item-dark' : ''">
                      <v-icon :color="overallConclusion.color" class="mr-2">
                        {{ overallConclusion.isFake ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                      </v-icon>
                      <span class="text-body-1" :class="overallConclusion.isFake ? 'error--text' : 'success--text'">
                        {{ overallConclusion.label }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Action buttons -->
                <div class="d-flex flex-wrap gap-4">
                  <v-btn
                    color="primary"
                    variant="elevated"
                    class="px-8 py-2"
                    rounded="pill"
                    prepend-icon="mdi-file-document-outline"
                    elevation="2"
                    @click="downloadReport"
                  >
                    查看报告
                  </v-btn>
                  <v-btn
                    :color="isDarkMode ? 'green-darken-2' : 'success'"
                    variant="elevated"
                    class="px-8 py-2"
                    rounded="pill"
                    prepend-icon="mdi-send"
                    elevation="2"
                    :disabled="textList.length === 0"
                    @click="openReviewDialog"
                  >
                    提交人工审核
                  </v-btn>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Paper Text Section ========== -->
    <template v-if="hasPaperResults && (taskType === 'paper_text' || taskType === 'multi_material')">
      <!-- Statistics Row -->
      <v-row class="mb-6">
        <v-col cols="12" md="3">
          <v-card elevation="2" rounded="lg" class="text-center pa-4">
            <div class="text-h4 primary--text">{{ paperStatistics.total }}</div>
            <div class="text-body-2 text-grey mt-1">总段落数</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card elevation="2" rounded="lg" class="text-center pa-4" color="red-lighten-5">
            <div class="text-h4 error--text">{{ paperStatistics.high }}</div>
            <div class="text-body-2 text-grey mt-1">高风险段落</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card elevation="2" rounded="lg" class="text-center pa-4" color="orange-lighten-5">
            <div class="text-h4 warning--text">{{ paperStatistics.medium }}</div>
            <div class="text-body-2 text-grey mt-1">中风险段落</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card elevation="2" rounded="lg" class="text-center pa-4" color="green-lighten-5">
            <div class="text-h4 success--text">{{ paperStatistics.low }}</div>
            <div class="text-body-2 text-grey mt-1">低风险段落</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Paper content: left 8 cols + right 4 cols -->
      <v-row>
        <!-- Left Column -->
        <v-col cols="12" md="8">
          <!-- Paragraph AI Analysis Card -->
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="d-flex justify-space-between pa-6">
              <div class="d-flex align-center">
                <v-icon color="primary" class="mr-2">mdi-text-box-search</v-icon>
                <span class="text-h6">段落AI生成分析</span>
              </div>
              <v-chip size="small" color="info">
                <v-icon start>mdi-information</v-icon>
                点击段落查看详情
              </v-chip>
            </v-card-title>
            <v-card-text class="pa-6">
              <div v-if="allPaperParagraphs.length === 0" class="text-center text-grey py-8">
                暂无段落分析数据
              </div>
              <div v-else class="paragraph-container">
                <div
                  v-for="(para, index) in allPaperParagraphs"
                  :key="index"
                  class="paragraph-item"
                  :class="getProbabilityClass(para.ai_probability)"
                  @click="showParagraphDetail(para)"
                >
                  <div class="paragraph-header">
                    <div class="paragraph-number">
                      <v-chip :color="getProbabilityColor(para.ai_probability)" size="small" label>
                        段落 {{ para.paragraph_index }}
                      </v-chip>
                    </div>
                    <div class="paragraph-probability">
                      <v-chip
                        :color="getProbabilityColor(para.ai_probability)"
                        size="small"
                        variant="outlined"
                      >
                        <v-icon start size="small">mdi-brain</v-icon>
                        AI概率: {{ (para.ai_probability * 100).toFixed(1) }}%
                      </v-chip>
                    </div>
                  </div>
                  <div class="paragraph-text">{{ para.text }}</div>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Factual Fake Reason Card -->
          <v-card
            v-for="(reason, idx) in factualFakeReasons"
            :key="'factual-' + idx"
            class="mb-6"
            elevation="2"
            rounded="lg"
            color="orange-lighten-5"
          >
            <v-card-title class="pa-6">
              <v-icon start color="warning">mdi-alert-circle</v-icon>
              <span class="text-h6">事实性鉴伪分析</span>
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="text-body-1">{{ reason }}</div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Right Column -->
        <v-col cols="12" md="4">
          <!-- Risk Distribution -->
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="pa-6">
              <span class="text-h6">风险分布</span>
            </v-card-title>
            <v-card-text class="pa-6">
              <v-progress-linear
                v-if="paperStatistics.total > 0"
                :model-value="(paperStatistics.high / paperStatistics.total) * 100"
                color="error"
                height="25"
                class="mb-4"
              >
                <template #default="{ value }">
                  <strong>高风险: {{ paperStatistics.high }} ({{ value.toFixed(0) }}%)</strong>
                </template>
              </v-progress-linear>

              <v-progress-linear
                v-if="paperStatistics.total > 0"
                :model-value="(paperStatistics.medium / paperStatistics.total) * 100"
                color="warning"
                height="25"
                class="mb-4"
              >
                <template #default="{ value }">
                  <strong>中风险: {{ paperStatistics.medium }} ({{ value.toFixed(0) }}%)</strong>
                </template>
              </v-progress-linear>

              <v-progress-linear
                v-if="paperStatistics.total > 0"
                :model-value="(paperStatistics.low / paperStatistics.total) * 100"
                color="success"
                height="25"
              >
                <template #default="{ value }">
                  <strong>低风险: {{ paperStatistics.low }} ({{ value.toFixed(0) }}%)</strong>
                </template>
              </v-progress-linear>

              <div v-if="paperStatistics.total === 0" class="text-center text-grey py-4">
                暂无风险分布数据
              </div>
            </v-card-text>
          </v-card>

          <!-- High Risk TOP5 -->
          <v-card elevation="2" rounded="lg">
            <v-card-title class="pa-6">
              <span class="text-h6">高风险段落TOP5</span>
            </v-card-title>
            <v-card-text class="pa-6">
              <v-list density="compact" v-if="topRiskParagraphs.length > 0">
                <v-list-item
                  v-for="(para, index) in topRiskParagraphs"
                  :key="index"
                  @click="showParagraphDetail(para)"
                  class="method-item"
                >
                  <template #prepend>
                    <v-icon :color="getProbabilityColor(para.ai_probability)">
                      mdi-format-paint
                    </v-icon>
                  </template>
                  <v-list-item-title>
                    段落 {{ para.paragraph_index }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ (para.ai_probability * 100).toFixed(1) }}% - {{ getProbabilityLevel(para.ai_probability) }}
                  </v-list-item-subtitle>
                  <template #append>
                    <v-chip
                      :color="getProbabilityColor(para.ai_probability)"
                      size="small"
                    >
                      {{ (para.ai_probability * 100).toFixed(1) }}%
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
              <div v-else class="text-center text-grey py-4">
                暂无高风险段落
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- ========== Review Text Section ========== -->
    <template v-if="hasReviewResults && (taskType === 'review_text' || taskType === 'multi_material')">
      <v-row>
        <!-- Left Column -->
        <v-col cols="12" md="8">
          <!-- Template Tendency Analysis Card -->
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="pa-6">
              <v-icon :color="templateLevel.color" class="mr-2">
                {{ templateLevel.icon }}
              </v-icon>
              <span class="text-h6">模板化倾向分析</span>
            </v-card-title>
            <v-card-text class="pa-6">
              <!-- Gauge -->
              <div class="d-flex flex-column align-center mb-6">
                <v-progress-circular
                  :model-value="avgTemplateScore * 100"
                  :size="250"
                  :width="25"
                  :color="templateLevel.color"
                  class="mb-4"
                >
                  <div class="text-center">
                    <div class="text-h2">{{ (avgTemplateScore * 100).toFixed(0) }}%</div>
                    <div class="text-h6">{{ templateLevel.level }}</div>
                  </div>
                </v-progress-circular>

                <v-chip :color="templateLevel.color" size="large">
                  <v-icon start>mdi-gauge</v-icon>
                  模板化倾向评分: {{ (avgTemplateScore * 100).toFixed(1) }}%
                </v-chip>
              </div>

              <!-- Score explanation -->
              <v-alert :color="templateLevel.color" variant="tonal" class="mb-4">
                <template #prepend>
                  <v-icon>mdi-information</v-icon>
                </template>
                <div class="text-body-1">
                  <strong>评分说明：</strong>
                  <ul class="mt-2">
                    <li>0-40%：低度模板化，Review个性化程度高，建议保持</li>
                    <li>40-70%：中度模板化，Review存在一定模板化痕迹，建议改进</li>
                    <li>70-100%：高度模板化，Review模板化严重，需要重新撰写</li>
                  </ul>
                </div>
              </v-alert>

              <!-- Suggestion -->
              <v-alert color="info" variant="tonal">
                <template #prepend>
                  <v-icon>mdi-lightbulb</v-icon>
                </template>
                <div class="text-body-1">
                  <strong>改进建议：</strong>
                  {{ getTemplateSuggestion(avgTemplateScore) }}
                </div>
              </v-alert>
            </v-card-text>
          </v-card>

          <!-- Template Analysis Reason Card -->
          <v-card
            v-for="(tplData, idx) in reviewTemplateData"
            :key="'template-reason-' + idx"
            class="mb-6"
            elevation="2"
            rounded="lg"
          >
            <v-card-title class="pa-6">
              <v-icon start color="primary">mdi-text-box-search</v-icon>
              <span class="text-h6">模板化分析原因</span>
              <v-chip v-if="reviewTemplateData.length > 1" size="small" class="ml-2">
                资源 #{{ tplData.resource_id }}
              </v-chip>
            </v-card-title>
            <v-card-text class="pa-6">
              <div v-if="tplData.reason" class="text-body-1 analysis-text">
                {{ tplData.reason }}
              </div>
              <div v-else class="text-center text-grey py-4">
                暂无模板化分析原因
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Right Column -->
        <v-col cols="12" md="4">
          <!-- Score Level Distribution -->
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="pa-6">
              <span class="text-h6">评分等级分布</span>
            </v-card-title>
            <v-card-text class="pa-6">
              <div class="score-distribution">
                <div class="score-item">
                  <div class="score-label">低度模板化 (0-40%)</div>
                  <v-progress-linear
                    :model-value="avgTemplateScore <= 0.4 ? 100 : 0"
                    color="success"
                    height="20"
                  >
                    <template #default="{ value }">
                      <span v-if="value > 0">{{ templateLevel.level === '低度模板化' ? '当前状态' : '0%' }}</span>
                    </template>
                  </v-progress-linear>
                </div>

                <div class="score-item">
                  <div class="score-label">中度模板化 (40-70%)</div>
                  <v-progress-linear
                    :model-value="avgTemplateScore > 0.4 && avgTemplateScore <= 0.7 ? 100 : 0"
                    color="warning"
                    height="20"
                  >
                    <template #default="{ value }">
                      <span v-if="value > 0">{{ templateLevel.level === '中度模板化' ? '当前状态' : '0%' }}</span>
                    </template>
                  </v-progress-linear>
                </div>

                <div class="score-item">
                  <div class="score-label">高度模板化 (70-100%)</div>
                  <v-progress-linear
                    :model-value="avgTemplateScore > 0.7 ? 100 : 0"
                    color="error"
                    height="20"
                  >
                    <template #default="{ value }">
                      <span v-if="value > 0">{{ templateLevel.level === '高度模板化' ? '当前状态' : '0%' }}</span>
                    </template>
                  </v-progress-linear>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Quality Metrics -->
          <v-card elevation="2" rounded="lg">
            <v-card-title class="pa-6">
              <span class="text-h6">质量评估指标</span>
            </v-card-title>
            <v-card-text class="pa-6">
              <v-list density="compact">
                <v-list-item>
                  <template #prepend>
                    <v-icon color="primary">mdi-star</v-icon>
                  </template>
                  <v-list-item-title>个性化程度</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ ((1 - avgTemplateScore) * 100).toFixed(1) }}%
                  </v-list-item-subtitle>
                  <template #append>
                    <v-chip :color="(1 - avgTemplateScore) > 0.5 ? 'success' : 'warning'" size="small">
                      {{ ((1 - avgTemplateScore) * 100).toFixed(1) }}%
                    </v-chip>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template #prepend>
                    <v-icon color="primary">mdi-pencil</v-icon>
                  </template>
                  <v-list-item-title>专业深度</v-list-item-title>
                  <v-list-item-subtitle>
                    基于{{ avgTemplateScore < 0.5 ? '高' : '中低' }}模板化倾向评估
                  </v-list-item-subtitle>
                  <template #append>
                    <v-chip :color="avgTemplateScore < 0.5 ? 'success' : 'warning'" size="small">
                      {{ avgTemplateScore < 0.5 ? '优秀' : '一般' }}
                    </v-chip>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template #prepend>
                    <v-icon color="primary">mdi-text-box</v-icon>
                  </template>
                  <v-list-item-title>内容质量</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ avgTemplateScore < 0.4 ? '高质量原创内容' : '存在模板化内容' }}
                  </v-list-item-subtitle>
                  <template #append>
                    <v-chip :color="avgTemplateScore < 0.4 ? 'success' : 'warning'" size="small">
                      {{ avgTemplateScore < 0.4 ? '优秀' : '一般' }}
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- ========== Dimensions Card ========== -->
    <v-row v-if="dimensions && Array.isArray(dimensions) && dimensions.length > 0">
      <v-col cols="12">
        <v-card class="mb-6" elevation="2" rounded="lg">
          <v-card-title class="pa-6">
            <v-icon color="primary" class="mr-2">mdi-chart-box</v-icon>
            <span class="text-h6">检测维度分析</span>
          </v-card-title>
          <v-card-text class="pa-6">
            <v-row>
              <v-col
                v-for="(dim, idx) in dimensions"
                :key="idx"
                cols="12"
                sm="6"
                md="4"
              >
                <v-card variant="outlined" rounded="lg" class="pa-4">
                  <div class="text-subtitle-1 font-weight-bold mb-2">{{ dim.name || `维度 ${idx + 1}` }}</div>
                  <v-chip
                    v-if="dim.score !== undefined"
                    :color="dim.score > 0.7 ? 'error' : dim.score > 0.4 ? 'warning' : 'success'"
                    size="small"
                    class="mb-2"
                  >
                    评分: {{ (dim.score * 100).toFixed(1) }}%
                  </v-chip>
                  <div v-if="dim.summary" class="text-body-2 text-grey">{{ dim.summary }}</div>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Evidence Card ========== -->
    <v-row v-if="evidence">
      <v-col cols="12">
        <v-card class="mb-6" elevation="2" rounded="lg">
          <v-card-title class="pa-6">
            <v-icon color="info" class="mr-2">mdi-file-document</v-icon>
            <span class="text-h6">检测证据</span>
          </v-card-title>
          <v-card-text class="pa-6">
            <v-card variant="outlined">
              <v-card-text>
                <pre class="evidence-pre">{{ typeof evidence === 'string' ? evidence : JSON.stringify(evidence, null, 2) }}</pre>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== LLM Analysis Card ========== -->
    <v-row v-if="llmAnalysis">
      <v-col cols="12">
        <v-card class="mb-6" elevation="2" rounded="lg">
          <v-card-title class="pa-6">
            <v-icon color="purple" class="mr-2">mdi-robot</v-icon>
            <span class="text-h6">大模型分析</span>
            <v-chip
              v-if="llmAnalysis.risk_level"
              :color="llmAnalysis.risk_level === 'high' ? 'error' : llmAnalysis.risk_level === 'medium' ? 'warning' : 'success'"
              size="small"
              class="ml-4"
            >
              {{ llmAnalysis.risk_level === 'high' ? '高风险' : llmAnalysis.risk_level === 'medium' ? '中风险' : '低风险' }}
            </v-chip>
          </v-card-title>
          <v-card-text class="pa-6">
            <!-- If it's a string, just display it -->
            <div v-if="typeof llmAnalysis === 'string'" class="text-body-1 analysis-text">
              {{ llmAnalysis }}
            </div>
            <!-- If it's an object, show structured key-value -->
            <div v-else-if="typeof llmAnalysis === 'object'">
              <v-row>
                <v-col
                  v-for="(value, key) in llmAnalysis"
                  :key="String(key)"
                  cols="12"
                  sm="6"
                >
                  <div class="llm-field">
                    <div class="text-subtitle-2 font-weight-bold mb-1">{{ getChineseLabel(String(key)) }}</div>
                    <v-card variant="outlined" rounded="lg" class="pa-3">
                      <div class="text-body-2">{{ formatLlmAnalysisValue(value) }}</div>
                    </v-card>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Paragraph Detail Dialog ========== -->
    <v-dialog v-model="showParagraphDialog" max-width="800">
      <v-card v-if="selectedParagraph" rounded="lg">
        <v-card-title class="pa-6 d-flex align-center">
          <v-icon :color="getProbabilityColor(selectedParagraph.ai_probability)" class="mr-2">
            {{ selectedParagraph.ai_probability > 0.5 ? 'mdi-alert-circle' : 'mdi-information' }}
          </v-icon>
          <span class="text-h6">段落 {{ selectedParagraph.paragraph_index }} 详情</span>
          <v-spacer />
          <v-btn icon="mdi-close" variant="text" @click="showParagraphDialog = false" />
        </v-card-title>

        <v-card-text class="pa-6">
          <!-- AI probability chips -->
          <div class="mb-4">
            <v-chip :color="getProbabilityColor(selectedParagraph.ai_probability)" size="large">
              <v-icon start>mdi-brain</v-icon>
              AI生成概率: {{ (selectedParagraph.ai_probability * 100).toFixed(1) }}%
            </v-chip>
            <v-chip
              :color="getProbabilityColor(selectedParagraph.ai_probability)"
              size="large"
              class="ml-2"
            >
              {{ getProbabilityLevel(selectedParagraph.ai_probability) }}
            </v-chip>
          </div>

          <!-- Paragraph text -->
          <div class="mb-4">
            <h3 class="text-h6 mb-2">段落内容</h3>
            <div class="paragraph-detail-text">{{ selectedParagraph.text }}</div>
          </div>

          <!-- AI judgment reason -->
          <div class="mb-4">
            <h3 class="text-h6 mb-2">AI判断原因</h3>
            <v-alert :color="getProbabilityColor(selectedParagraph.ai_probability)" variant="tonal">
              {{ selectedParagraph.reason }}
            </v-alert>
          </div>

          <!-- Probability visual -->
          <div>
            <h3 class="text-h6 mb-2">AI生成概率可视化</h3>
            <v-progress-linear
              :model-value="selectedParagraph.ai_probability * 100"
              :color="getProbabilityColor(selectedParagraph.ai_probability)"
              height="30"
            >
              <template #default="{ value }">
                <strong>{{ value.toFixed(1) }}%</strong>
              </template>
            </v-progress-linear>
          </div>
        </v-card-text>

        <v-card-actions class="pa-6 pt-0">
          <v-spacer />
          <v-btn color="primary" @click="showParagraphDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ========== Review Submission Dialog ========== -->
    <v-dialog v-model="showReviewDialog" max-width="700" persistent>
      <v-card rounded="lg">
        <v-card-title class="pa-6 d-flex align-center">
          <v-icon color="success" class="mr-2">mdi-send</v-icon>
          <span class="text-h6">提交人工审核</span>
          <v-spacer />
          <v-btn icon="mdi-close" variant="text" @click="showReviewDialog = false" />
        </v-card-title>

        <v-card-text class="pa-6">
          <!-- Text ID selection -->
          <div class="mb-4">
            <div class="text-subtitle-1 font-weight-bold mb-2">选择检测文本</div>
            <v-list variant="outlined" rounded="lg" density="compact" class="border">
              <v-list-item
                v-for="item in textList"
                :key="item.resource_id"
                @click="toggleTextId(item.resource_id)"
              >
                <template #prepend>
                  <v-checkbox
                    :model-value="selectedTextIds.includes(item.resource_id)"
                    @click.stop
                    @update:model-value="toggleTextId(item.resource_id)"
                    color="primary"
                    hide-details
                  />
                </template>
                <v-list-item-title>
                  文本资源 #{{ item.resource_id }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  类型: {{ item.text_type === 'paper_text' ? '论文文本' : item.text_type === 'review_text' ? '评审文本' : item.text_type }}
                  <span v-if="item.is_fake" class="error--text ml-2">疑似AI生成</span>
                </v-list-item-subtitle>
                <template #append>
                  <v-chip
                    :color="item.is_fake ? 'error' : 'success'"
                    size="small"
                  >
                    {{ (item.confidence_score * 100).toFixed(1) }}%
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </div>

          <!-- Reviewer selection -->
          <div class="mb-4">
            <div class="text-subtitle-1 font-weight-bold mb-2">选择审核人员</div>
            <v-autocomplete
              v-model="selectedReviewers"
              :items="filteredReviewers"
              v-model:search="reviewSearchQuery"
              item-title="username"
              item-value="id"
              label="搜索审核人员"
              multiple
              chips
              closable-chips
              hide-details
              variant="outlined"
            >
              <template #chip="{ props: chipProps, item }">
                <v-chip v-bind="chipProps" :prepend-avatar="getImageUrl(item.raw.avatar)">
                  {{ item.raw.username }}
                </v-chip>
              </template>
              <template #item="{ props: itemProps, item }">
                <v-list-item v-bind="itemProps" :prepend-avatar="getImageUrl(item.raw.avatar)" :title="item.raw.username" />
              </template>
            </v-autocomplete>
          </div>

          <!-- Reason -->
          <div>
            <div class="text-subtitle-1 font-weight-bold mb-2">审核原因</div>
            <v-textarea
              v-model="reviewReason"
              label="请输入提交审核的原因（选填）"
              variant="outlined"
              rows="3"
              hide-details
            />
          </div>
        </v-card-text>

        <v-card-actions class="pa-6 pt-0">
          <v-spacer />
          <v-btn variant="text" @click="showReviewDialog = false">取消</v-btn>
          <v-btn
            color="success"
            variant="elevated"
            :disabled="!canSubmitReview"
            :loading="submittingReview"
            @click="submitReview"
          >
            提交审核
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.detection-summary {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.custom-progress {
  --v-progress-circular-size: 160px;
  --v-progress-circular-underlay-color: v-bind(isDarkMode ? 'rgba(255, 255, 255, 0.05)' : '#f5f5f5');
  transition: all 0.3s ease;
}

.border-r {
  border-right: 1px solid #e5e7eb;
}

.responsive-text {
  font-size: clamp(1rem, 2vw, 1.5rem);
}

.text-subtitle-2.responsive-text {
  font-size: clamp(0.75rem, 1.5vw, 1rem);
}

.info-item {
  padding: 8px 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.info-item-dark {
  background-color: rgba(255, 255, 255, 0.05);
}

.paragraph-container {
  max-height: 800px;
  overflow-y: auto;
}

.paragraph-item {
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.paragraph-item:hover {
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.high-probability {
  background-color: rgba(255, 0, 0, 0.05);
  border-left: 4px solid #f44336;
}

.medium-probability {
  background-color: rgba(255, 165, 0, 0.05);
  border-left: 4px solid #ff9800;
}

.low-probability {
  background-color: rgba(0, 128, 0, 0.05);
  border-left: 4px solid #4caf50;
}

.paragraph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.paragraph-number {
  font-weight: bold;
}

.paragraph-probability {
  font-size: 14px;
}

.paragraph-text {
  line-height: 1.8;
  color: #333;
  text-align: justify;
}

.paragraph-detail-text {
  line-height: 1.8;
  color: #333;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.method-item {
  cursor: pointer;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.method-item:hover {
  background-color: #f5f5f5;
}

.analysis-text {
  line-height: 1.8;
  color: #333;
  text-align: justify;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.score-distribution {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.score-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.score-label {
  font-size: 14px;
  font-weight: 500;
  color: #666;
}

.evidence-pre {
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  font-family: "Courier New", Courier, monospace;
  font-size: 0.9rem;
}

.llm-field {
  margin-bottom: 8px;
}

.border {
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.gap-2 {
  gap: 8px;
}

.gap-4 {
  gap: 16px;
}
</style>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTheme } from 'vuetify'
import { useSnackbarStore } from '@/stores/snackbar'
import { useUserStore } from '@/stores/user'
import publisher from '@/api/publisher'
import { useRouter } from 'vue-router'
import { resolveImageUrl } from '@/utils/preview-url'

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

// --- Extract result payload ---
const result = computed(() => props.taskMeta?.result || {})

// Overall
const overall = computed(() => result.value?.overall || {})
const isFake = computed(() => {
  if (props.taskMeta?.overall_is_fake !== undefined) return props.taskMeta.overall_is_fake
  return overall.value?.is_fake ?? false
})
const confidenceScore = computed(() => {
  if (props.taskMeta?.confidence_score !== undefined) return props.taskMeta.confidence_score
  return overall.value?.confidence_score ?? 0
})
const riskLevel = computed(() => overall.value?.risk_level || 'low')

const overallConclusion = computed(() => {
  const score = confidenceScore.value
  const fake = isFake.value
  return {
    isFake: fake,
    confidence: (score * 100).toFixed(1) + '%',
    color: fake ? 'error' : 'success',
    label: fake ? '检测到学术不端风险' : '未检测到明显风险'
  }
})

// Summary text
const summaryText = computed(() => {
  return props.taskMeta?.summary || result.value?.summary || ''
})

// LLM analysis
const llmAnalysis = computed(() => {
  return result.value?.llm_analysis || props.taskMeta?.ai_response?.llm_analysis || null
})

// Cross material analysis
const crossMaterialAnalysis = computed(() => {
  return result.value?.cross_material_analysis || null
})

// AI contribution
const aiContribution = computed(() => {
  return result.value?.ai_contribution || []
})

// Material cards
const materialCards = computed(() => {
  return result.value?.material_cards || []
})

// Evidence
const evidence = computed(() => {
  return result.value?.evidence || null
})

// Dimensions
const dimensions = computed(() => {
  return result.value?.dimensions || []
})

// Validation info
const validation = computed(() => {
  return result.value?.validation || null
})

// --- Sections visibility ---
const hasPaperSection = computed(() => {
  return materialCards.value.some((c: any) => c.type === 'paper') ||
    (evidence.value?.per_section || []).some((s: any) => (s.item_id || '').startsWith('multi_paper'))
})

const hasReviewSection = computed(() => {
  return materialCards.value.some((c: any) => c.type === 'review') ||
    (evidence.value?.per_section || []).some((s: any) => (s.item_id || '').startsWith('multi_review'))
})

const hasImageSection = computed(() => {
  return materialCards.value.some((c: any) => c.type === 'image')
})

// --- Paper analysis data ---
const paperParagraphs = computed(() => {
  const perSection = evidence.value?.per_section || []
  return perSection
    .filter((s: any) => (s.item_id || '').includes('paper'))
    .map((s: any) => ({
      id: s.item_id,
      isAigc: s.is_aigc,
      confidence: s.confidence_score,
      aigcProb: s.probabilities?.aigc || 0,
      humanProb: s.probabilities?.human || 0,
    }))
    .sort((a: any, b: any) => b.aigcProb - a.aigcProb)
})

const paperStatistics = computed(() => {
  const paras = paperParagraphs.value
  const total = paras.length
  const high = paras.filter((p: any) => p.aigcProb > 0.8).length
  const medium = paras.filter((p: any) => p.aigcProb > 0.5 && p.aigcProb <= 0.8).length
  const low = paras.filter((p: any) => p.aigcProb <= 0.5).length
  return { total, high, medium, low }
})

const paperCard = computed(() => {
  return materialCards.value.find((c: any) => c.type === 'paper') || null
})

// --- Review analysis data ---
const reviewParagraphs = computed(() => {
  const perSection = evidence.value?.per_section || []
  return perSection
    .filter((s: any) => (s.item_id || '').includes('review'))
    .map((s: any) => ({
      id: s.item_id,
      isAigc: s.is_aigc,
      confidence: s.confidence_score,
      aigcProb: s.probabilities?.aigc || 0,
      humanProb: s.probabilities?.human || 0,
    }))
})

const avgReviewAigc = computed(() => {
  if (reviewParagraphs.value.length === 0) return 0
  const sum = reviewParagraphs.value.reduce((acc: number, p: any) => acc + p.aigcProb, 0)
  return sum / reviewParagraphs.value.length
})

const reviewCard = computed(() => {
  return materialCards.value.find((c: any) => c.type === 'review') || null
})

const templateLevel = computed(() => {
  const score = avgReviewAigc.value
  if (score > 0.7) return { level: '高度风险', color: 'error', icon: 'mdi-alert-octagon' }
  if (score > 0.4) return { level: '中度风险', color: 'warning', icon: 'mdi-alert' }
  return { level: '低风险', color: 'success', icon: 'mdi-check-circle' }
})

// --- Image analysis data ---
const imageCard = computed(() => {
  return materialCards.value.find((c: any) => c.type === 'image') || null
})

const imageItems = computed(() => {
  if (!imageCard.value) return []
  return imageCard.value.images || imageCard.value.results || []
})

// --- Reviewer selection ---
interface Reviewer {
  id: number
  username: string
  avatar: string
}

const allReviewers = ref<Reviewer[]>([])
const showReviewDialog = ref(false)
const selectedReviewers = ref<number[]>([])
const reviewReason = ref('')
const submittingReview = ref(false)
const reviewSearchQuery = ref('')

const canSubmitReview = computed(() => selectedReviewers.value.length > 0)

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

function getImageUrl(url: string): string {
  return resolveImageUrl(url)
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
    risk_factors: '风险因素',
    cross_checks: '交叉验证',
    mismatches: '不匹配项',
    recommendations: '建议',
    suspicious_patterns: '可疑模式',
  }
  return map[key] || key
}

function formatLlmAnalysisValue(value: unknown): string {
  if (value === null || value === undefined) return ''
  if (typeof value === 'string') return value
  if (typeof value === 'number') return String(value)
  if (typeof value === 'boolean') return value ? '是' : '否'
  if (Array.isArray(value)) return value.join('\n')
  try {
    return JSON.stringify(value, null, 2)
  } catch {
    return String(value)
  }
}

function openReviewDialog() {
  selectedReviewers.value = []
  reviewReason.value = ''
  showReviewDialog.value = true
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
      task_id: props.taskId,
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
const loading = ref(true)

onMounted(async () => {
  loading.value = true
  try {
    const resp = await publisher.getReviewers({ publisher_id: userStore.id })
    allReviewers.value = Array.isArray(resp.data?.reviewers) ? resp.data.reviewers : []
  } catch (err) {
    console.error('获取审核人员失败:', err)
    allReviewers.value = []
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
            <!-- Left: progress ring -->
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
              </div>
            </v-col>

            <!-- Right: info and buttons -->
            <v-col cols="8" class="pl-8">
              <div class="d-flex flex-column justify-space-between h-100">
                <div class="task-info mb-8">
                  <div class="text-h6 mb-4">多材料综合检测结果</div>
                  <div class="d-flex flex-column gap-2">
                    <div class="info-item d-flex align-center" :class="isDarkMode ? 'info-item-dark' : ''">
                      <v-icon :color="isDarkMode ? 'grey-lighten-1' : 'grey-darken-2'" class="mr-2">mdi-clock-outline</v-icon>
                      <span class="text-body-1">检测编号：{{ taskId }}</span>
                    </div>
                    <div v-if="overallConclusion" class="info-item d-flex align-center" :class="isDarkMode ? 'info-item-dark' : ''">
                      <v-icon :color="overallConclusion.color" class="mr-2">
                        {{ overallConclusion.isFake ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                      </v-icon>
                      <span class="text-body-1" :class="overallConclusion.isFake ? 'error--text' : 'success--text'">
                        {{ overallConclusion.label }}
                      </span>
                    </div>
                    <div v-if="riskLevel" class="info-item d-flex align-center" :class="isDarkMode ? 'info-item-dark' : ''">
                      <v-icon :color="riskLevel === 'high' ? 'error' : riskLevel === 'medium' ? 'warning' : 'success'" class="mr-2">
                        mdi-shield-alert
                      </v-icon>
                      <span class="text-body-1">
                        风险等级：{{ riskLevel === 'high' ? '高风险' : riskLevel === 'medium' ? '中风险' : '低风险' }}
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

    <!-- ========== Summary Card ========== -->
    <v-row v-if="summaryText">
      <v-col cols="12">
        <v-card class="mb-6" elevation="2" rounded="lg">
          <v-card-title class="pa-6">
            <v-icon color="primary" class="mr-2">mdi-text-box-check</v-icon>
            <span class="text-h6">综合摘要</span>
          </v-card-title>
          <v-card-text class="pa-6">
            <div class="text-body-1 analysis-text">{{ summaryText }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Material Cards Overview ========== -->
    <v-row v-if="materialCards.length > 0" class="mb-6">
      <v-col
        v-for="(card, idx) in materialCards"
        :key="idx"
        cols="12"
        md="4"
      >
        <v-card elevation="2" rounded="lg" class="text-center pa-4">
          <v-icon
            :color="card.type === 'paper' ? 'primary' : card.type === 'review' ? 'warning' : 'info'"
            size="48"
            class="mb-2"
          >
            {{ card.type === 'paper' ? 'mdi-file-document' : card.type === 'review' ? 'mdi-comment-text' : 'mdi-image-multiple' }}
          </v-icon>
          <div class="text-h6 mb-1">{{ card.label || (card.type === 'paper' ? '论文材料' : card.type === 'review' ? '评审材料' : '图片材料') }}</div>
          <div v-if="card.summary" class="text-body-2 text-grey mb-2">{{ card.summary }}</div>
          <v-chip
            v-if="card.score !== undefined"
            :color="getProbabilityColor(card.score)"
            size="small"
          >
            风险评分: {{ (card.score * 100).toFixed(1) }}%
          </v-chip>
          <div v-if="card.file_count" class="text-caption text-grey mt-1">
            文件数: {{ card.file_count }}
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Cross Material Analysis ========== -->
    <v-row v-if="crossMaterialAnalysis">
      <v-col cols="12">
        <v-card class="mb-6" elevation="2" rounded="lg">
          <v-card-title class="pa-6">
            <v-icon color="info" class="mr-2">mdi-compare-horizontal</v-icon>
            <span class="text-h6">交叉验证分析</span>
          </v-card-title>
          <v-card-text class="pa-6">
            <!-- cross_checks -->
            <div v-if="crossMaterialAnalysis.cross_checks && crossMaterialAnalysis.cross_checks.length > 0" class="mb-4">
              <div class="text-subtitle-1 font-weight-bold mb-2">交叉验证发现</div>
              <v-list density="compact">
                <v-list-item
                  v-for="(item, idx) in crossMaterialAnalysis.cross_checks"
                  :key="'cc-' + idx"
                >
                  <template #prepend>
                    <v-icon color="info" class="mr-2">mdi-link-variant</v-icon>
                  </template>
                  <v-list-item-title>{{ item }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </div>

            <!-- mismatches -->
            <div v-if="crossMaterialAnalysis.mismatches && crossMaterialAnalysis.mismatches.length > 0" class="mb-4">
              <div class="text-subtitle-1 font-weight-bold mb-2">多材料不匹配项</div>
              <v-list density="compact">
                <v-list-item
                  v-for="(item, idx) in crossMaterialAnalysis.mismatches"
                  :key="'mm-' + idx"
                >
                  <template #prepend>
                    <v-icon color="warning" class="mr-2">mdi-alert</v-icon>
                  </template>
                  <v-list-item-title>{{ item }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </div>

            <!-- recommendations from cross analysis -->
            <div v-if="crossMaterialAnalysis.recommendations && crossMaterialAnalysis.recommendations.length > 0">
              <div class="text-subtitle-1 font-weight-bold mb-2">复核建议</div>
              <v-list density="compact">
                <v-list-item
                  v-for="(item, idx) in crossMaterialAnalysis.recommendations"
                  :key="'rec-' + idx"
                >
                  <template #prepend>
                    <v-icon color="success" class="mr-2">mdi-lightbulb</v-icon>
                  </template>
                  <v-list-item-title>{{ item }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </div>

            <!-- Fallback: display raw object if none of the above matched -->
            <div v-if="!crossMaterialAnalysis.cross_checks && !crossMaterialAnalysis.mismatches && !crossMaterialAnalysis.recommendations">
              <v-card variant="outlined">
                <v-card-text>
                  <pre class="evidence-pre">{{ JSON.stringify(crossMaterialAnalysis, null, 2) }}</pre>
                </v-card-text>
              </v-card>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Paper Analysis Section ========== -->
    <template v-if="hasPaperSection">
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="pa-6">
              <v-icon color="primary" class="mr-2">mdi-file-document-edit</v-icon>
              <span class="text-h6">论文文本分析</span>
              <v-chip v-if="paperCard && paperCard.score !== undefined" :color="getProbabilityColor(paperCard.score)" size="small" class="ml-4">
                AIGC评分: {{ (paperCard.score * 100).toFixed(1) }}%
              </v-chip>
            </v-card-title>
            <v-card-text class="pa-6">
              <div v-if="paperCard && paperCard.summary" class="text-body-1 mb-4">{{ paperCard.summary }}</div>

              <!-- Statistics row -->
              <v-row class="mb-4">
                <v-col cols="12" md="3">
                  <v-card variant="outlined" rounded="lg" class="text-center pa-3">
                    <div class="text-h5 primary--text">{{ paperStatistics.total }}</div>
                    <div class="text-caption text-grey">总段落数</div>
                  </v-card>
                </v-col>
                <v-col cols="12" md="3">
                  <v-card variant="outlined" rounded="lg" class="text-center pa-3" color="red-lighten-5">
                    <div class="text-h5 error--text">{{ paperStatistics.high }}</div>
                    <div class="text-caption text-grey">高风险</div>
                  </v-card>
                </v-col>
                <v-col cols="12" md="3">
                  <v-card variant="outlined" rounded="lg" class="text-center pa-3" color="orange-lighten-5">
                    <div class="text-h5 warning--text">{{ paperStatistics.medium }}</div>
                    <div class="text-caption text-grey">中风险</div>
                  </v-card>
                </v-col>
                <v-col cols="12" md="3">
                  <v-card variant="outlined" rounded="lg" class="text-center pa-3" color="green-lighten-5">
                    <div class="text-h5 success--text">{{ paperStatistics.low }}</div>
                    <div class="text-caption text-grey">低风险</div>
                  </v-card>
                </v-col>
              </v-row>

              <!-- Paragraph list -->
              <div v-if="paperParagraphs.length > 0">
                <div class="text-subtitle-1 font-weight-bold mb-3">段落AI生成分析</div>
                <div class="paragraph-container">
                  <div
                    v-for="(para, index) in paperParagraphs"
                    :key="index"
                    class="paragraph-item"
                    :class="para.aigcProb > 0.8 ? 'high-probability' : para.aigcProb > 0.5 ? 'medium-probability' : 'low-probability'"
                  >
                    <div class="paragraph-header">
                      <div class="paragraph-number">
                        <v-chip :color="getProbabilityColor(para.aigcProb)" size="small" label>
                          {{ para.id }}
                        </v-chip>
                      </div>
                      <div class="paragraph-probability">
                        <v-chip :color="getProbabilityColor(para.aigcProb)" size="small" variant="outlined">
                          <v-icon start size="small">mdi-brain</v-icon>
                          AI概率: {{ (para.aigcProb * 100).toFixed(1) }}%
                        </v-chip>
                      </div>
                    </div>
                    <div class="d-flex align-center gap-2 mt-2">
                      <v-progress-linear
                        :model-value="para.aigcProb * 100"
                        :color="getProbabilityColor(para.aigcProb)"
                        height="8"
                        rounded
                        class="flex-grow-1"
                      />
                      <v-chip :color="getProbabilityColor(para.aigcProb)" size="small">
                        {{ getProbabilityLevel(para.aigcProb) }}
                      </v-chip>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center text-grey py-4">
                暂无论文段落分析数据
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- ========== Review Analysis Section ========== -->
    <template v-if="hasReviewSection">
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="pa-6">
              <v-icon :color="templateLevel.color" class="mr-2">{{ templateLevel.icon }}</v-icon>
              <span class="text-h6">评审文本分析</span>
              <v-chip v-if="reviewCard && reviewCard.score !== undefined" :color="getProbabilityColor(reviewCard.score)" size="small" class="ml-4">
                AIGC评分: {{ (reviewCard.score * 100).toFixed(1) }}%
              </v-chip>
            </v-card-title>
            <v-card-text class="pa-6">
              <div v-if="reviewCard && reviewCard.summary" class="text-body-1 mb-4">{{ reviewCard.summary }}</div>

              <!-- Template tendency gauge -->
              <div class="d-flex flex-column align-center mb-6">
                <v-progress-circular
                  :model-value="avgReviewAigc * 100"
                  :size="200"
                  :width="20"
                  :color="templateLevel.color"
                  class="mb-4"
                >
                  <div class="text-center">
                    <div class="text-h3">{{ (avgReviewAigc * 100).toFixed(0) }}%</div>
                    <div class="text-subtitle-1">{{ templateLevel.level }}</div>
                  </div>
                </v-progress-circular>
                <v-chip :color="templateLevel.color" size="large">
                  <v-icon start>mdi-brain</v-icon>
                  AIGC倾向评分: {{ (avgReviewAigc * 100).toFixed(1) }}%
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
                    <li>0-40%：低风险，评审文本个性化程度高</li>
                    <li>40-70%：中风险，存在一定模板化或AI生成痕迹</li>
                    <li>70-100%：高风险，评审文本疑似AI生成或高度模板化</li>
                  </ul>
                </div>
              </v-alert>

              <!-- Review paragraphs detail -->
              <div v-if="reviewParagraphs.length > 0" class="mt-4">
                <div class="text-subtitle-1 font-weight-bold mb-3">评审文本段落分析</div>
                <div class="paragraph-container">
                  <div
                    v-for="(para, index) in reviewParagraphs"
                    :key="index"
                    class="paragraph-item"
                    :class="para.aigcProb > 0.8 ? 'high-probability' : para.aigcProb > 0.5 ? 'medium-probability' : 'low-probability'"
                  >
                    <div class="paragraph-header">
                      <div class="paragraph-number">
                        <v-chip :color="getProbabilityColor(para.aigcProb)" size="small" label>
                          {{ para.id }}
                        </v-chip>
                      </div>
                      <div class="paragraph-probability">
                        <v-chip :color="getProbabilityColor(para.aigcProb)" size="small" variant="outlined">
                          <v-icon start size="small">mdi-brain</v-icon>
                          AI概率: {{ (para.aigcProb * 100).toFixed(1) }}%
                        </v-chip>
                      </div>
                    </div>
                    <div class="d-flex align-center gap-2 mt-2">
                      <v-progress-linear
                        :model-value="para.aigcProb * 100"
                        :color="getProbabilityColor(para.aigcProb)"
                        height="8"
                        rounded
                        class="flex-grow-1"
                      />
                      <v-chip :color="getProbabilityColor(para.aigcProb)" size="small">
                        {{ getProbabilityLevel(para.aigcProb) }}
                      </v-chip>
                    </div>
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- ========== Image Analysis Section ========== -->
    <template v-if="hasImageSection">
      <v-row>
        <v-col cols="12">
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="pa-6">
              <v-icon color="info" class="mr-2">mdi-image-search</v-icon>
              <span class="text-h6">图片分析</span>
            </v-card-title>
            <v-card-text class="pa-6">
              <div v-if="imageCard && imageCard.summary" class="text-body-1 mb-4">{{ imageCard.summary }}</div>

              <!-- Image grid -->
              <div v-if="imageItems.length > 0" class="image-grid-container">
                <div class="d-flex flex-wrap gap-4">
                  <v-card
                    v-for="(img, idx) in imageItems"
                    :key="idx"
                    width="200"
                    elevation="2"
                    rounded="lg"
                    class="overflow-hidden"
                  >
                    <v-img
                      v-if="img.image_url || img.url"
                      :src="getImageUrl(img.image_url || img.url)"
                      height="150"
                      cover
                    >
                      <div class="image-verdict-overlay">
                        <v-chip
                          :color="img.is_fake ? 'error' : 'success'"
                          size="small"
                          class="ma-2"
                        >
                          <v-icon start size="small">{{ img.is_fake ? 'mdi-alert' : 'mdi-check' }}</v-icon>
                          {{ img.is_fake ? '疑似造假' : '正常' }}
                        </v-chip>
                      </div>
                    </v-img>
                    <v-card-text class="pa-2 text-center">
                      <div class="text-caption">
                        <v-chip
                          :color="getProbabilityColor(img.confidence || img.fake_probability || 0)"
                          size="small"
                        >
                          {{ ((img.confidence || img.fake_probability || 0) * 100).toFixed(1) }}%
                        </v-chip>
                      </div>
                      <div v-if="img.image_id" class="text-caption text-grey mt-1">
                        图片 #{{ img.image_id }}
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </div>
              <div v-else class="text-center text-grey py-4">
                暂无图片分析数据
              </div>
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

    <!-- ========== AI Contribution ========== -->
    <v-row v-if="aiContribution.length > 0">
      <v-col cols="12">
        <v-card class="mb-6" elevation="2" rounded="lg">
          <v-card-title class="pa-6">
            <v-icon color="purple" class="mr-2">mdi-robot</v-icon>
            <span class="text-h6">AI检测贡献</span>
          </v-card-title>
          <v-card-text class="pa-6">
            <v-list density="compact">
              <v-list-item
                v-for="(item, idx) in aiContribution"
                :key="idx"
              >
                <template #prepend>
                  <v-icon color="purple" class="mr-2">mdi-star-four-points</v-icon>
                </template>
                <v-list-item-title>{{ typeof item === 'string' ? item : JSON.stringify(item) }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Evidence Card ========== -->
    <v-row v-if="evidence && (typeof evidence === 'string' || (typeof evidence === 'object' && !Array.isArray(evidence?.per_section)))">
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
            <!-- String display -->
            <div v-if="typeof llmAnalysis === 'string'" class="text-body-1 analysis-text">
              {{ llmAnalysis }}
            </div>
            <!-- Raw text fallback -->
            <div v-else-if="llmAnalysis.raw_text" class="text-body-1 analysis-text">
              {{ llmAnalysis.raw_text }}
            </div>
            <!-- Structured key-value display -->
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
  --v-progress-circular-underway-color: v-bind(isDarkMode ? 'rgba(255, 255, 255, 0.05)' : '#f5f5f5');
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
  max-height: 600px;
  overflow-y: auto;
}

.paragraph-item {
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  cursor: default;
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
  margin-bottom: 8px;
}

.paragraph-number {
  font-weight: bold;
}

.paragraph-probability {
  font-size: 14px;
}

.image-grid-container {
  width: 100%;
}

.image-verdict-overlay {
  position: absolute;
  top: 0;
  left: 0;
}

.analysis-text {
  line-height: 1.8;
  color: #333;
  text-align: justify;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
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

.gap-2 {
  gap: 8px;
}

.gap-4 {
  gap: 16px;
}
</style>

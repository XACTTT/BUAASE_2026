<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
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
      text: s.text || '',
      title: s.title || '',
      pageNumber: s.page_number ?? null,
      sourceFile: s.source_file || '',
      labelName: s.label_name || '',
    }))
})

const paperSortMode = ref<'order' | 'risk'>('order')
const sortedPaperParagraphs = computed(() => {
  if (paperSortMode.value === 'risk') {
    return [...paperParagraphs.value].sort((a, b) => b.aigcProb - a.aigcProb)
  }
  return paperParagraphs.value
})

const selectedPaperId = ref<string | null>(null)
function selectPaperParagraph(id: string) {
  selectedPaperId.value = selectedPaperId.value === id ? null : id
}
const selectedPaperParagraph = computed(() => {
  if (!selectedPaperId.value) return null
  return paperParagraphs.value.find(p => p.id === selectedPaperId.value) || null
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
      text: s.text || '',
      title: s.title || '',
      pageNumber: s.page_number ?? null,
      sourceFile: s.source_file || '',
      labelName: s.label_name || '',
    }))
})

const reviewSortMode = ref<'order' | 'risk'>('order')
const sortedReviewParagraphs = computed(() => {
  if (reviewSortMode.value === 'risk') {
    return [...reviewParagraphs.value].sort((a, b) => b.aigcProb - a.aigcProb)
  }
  return reviewParagraphs.value
})

const selectedReviewId = ref<string | null>(null)
function selectReviewParagraph(id: string) {
  selectedReviewId.value = selectedReviewId.value === id ? null : id
}
const selectedReviewParagraph = computed(() => {
  if (!selectedReviewId.value) return null
  return reviewParagraphs.value.find(p => p.id === selectedReviewId.value) || null
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

const imageFakeCount = computed(() => imageItems.value.filter((img: any) => img.is_fake).length)
const imageNormalCount = computed(() => imageItems.value.filter((img: any) => img.result_id && !img.is_fake).length)
const imageDetectedCount = computed(() => imageItems.value.filter((img: any) => img.result_id).length)

// --- Image detail dialog ---
interface ImageItem {
  image_id: number
  image_url: string
  result_id?: number
  is_fake?: boolean
  confidence?: number
}

interface SubMethod {
  method: string
  probability: number
  mask_image: string
  mask_matrix: any
  visible: boolean
}

const showImageDetail = ref(false)
const selectedImage = ref<ImageItem | null>(null)
const imageDetailLoading = ref(false)
const imageDetailError = ref('')
const hasDetectionResult = ref(false)
const detectionStatus = ref('')
const activeTab = ref('analysis')
const llm = ref('')
const llm_image = ref('')
const ela = ref('')
const urn = ref<SubMethod[]>([])
const exif = ref({ photoshop_edited: false, time_modified: false, detection_time: null as string | null })
const activeOverlay = ref('')
const isOverlayVisible = ref(false)

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

// --- Image detail functions ---
const viewImageDetail = (img: ImageItem) => {
  selectedImage.value = img
  showImageDetail.value = true
  imageDetailError.value = ''
  if (img.image_id) {
    fetchImageDetection(img.image_id)
  }
}

const fetchImageDetection = async (imageId: number) => {
  imageDetailLoading.value = true
  imageDetailError.value = ''
  hasDetectionResult.value = false
  try {
    const response = (await publisher.getImageDetectionByImageId(imageId)).data
    hasDetectionResult.value = true
    detectionStatus.value = response.status || ''
    llm.value = response.llm || ''
    llm_image.value = response.llm_image || ''
    ela.value = response.ela_image || ''
    urn.value = (response.sub_methods || []).map((item: any) => ({
      ...item,
      visible: false,
    }))
    if (response.exif) {
      exif.value = {
        photoshop_edited: response.exif.photoshop_edited || false,
        time_modified: response.exif.time_modified || false,
        detection_time: response.timestamps || null,
      }
    }
  } catch (error: any) {
    if (error?.response?.status === 404) {
      hasDetectionResult.value = false
    } else {
      imageDetailError.value = '获取图片检测结果失败'
    }
    llm.value = ''
    llm_image.value = ''
    ela.value = ''
    urn.value = []
    detectionStatus.value = ''
  } finally {
    imageDetailLoading.value = false
  }
}

const toggleOverlay = (dimension: SubMethod) => {
  if (dimension.visible) {
    dimension.visible = false
    isOverlayVisible.value = false
    activeOverlay.value = ''
    return
  }
  urn.value.forEach(d => {
    if (d !== dimension) d.visible = false
  })
  dimension.visible = true
  isOverlayVisible.value = true
  activeOverlay.value = resolveImageUrl(dimension.mask_image)
}

const toggleImageDetailClose = () => {
  showImageDetail.value = false
  selectedImage.value = null
  llm.value = ''
  llm_image.value = ''
  ela.value = ''
  urn.value = []
  exif.value = { photoshop_edited: false, time_modified: false, detection_time: null }
  activeOverlay.value = ''
  isOverlayVisible.value = false
  activeTab.value = 'analysis'
  imageDetailError.value = ''
  hasDetectionResult.value = false
  detectionStatus.value = ''
}

const getSelectedImageUrl = (img: ImageItem | null) => {
  if (!img) return ''
  return resolveImageUrl(img.image_url)
}

const showRawJson = ref(false)

const copyRawJson = () => {
  const text = JSON.stringify(result.value, null, 2)
  navigator.clipboard.writeText(text).then(() => {
    snackbar.showMessage('已复制到剪贴板', 'success')
  }).catch(() => {
    snackbar.showMessage('复制失败', 'error')
  })
}

// --- Helpers ---
function getProbabilityColor(probability: number): string {
  if (probability > 0.8) return 'error'
  if (probability > 0.5) return 'warning'
  return 'success'
}

const SUB_METHOD_LABELS: Record<string, string> = {
  splicing: '拼接',
  blurring: '模糊',
  bruteforce: '暴力',
  contrast: '对比度',
  inpainting: '修复',
}
function getSubMethodLabel(method: string): string {
  return SUB_METHOD_LABELS[method] || method
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
    if (response.status !== 200) {
      const msg = response.data?.detail || '报告生成中，请稍后重试'
      snackbar.showMessage(msg, 'warning')
      return
    }
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
    snackbar.showMessage('报告下载成功', 'success')
  } catch (error) {
    snackbar.showMessage('报告下载失败', 'error')
  }
}

const submitReview = async () => {
  if (!canSubmitReview.value) return
  submittingReview.value = true
  try {
    const payload: any = {
      task_id: props.taskId,
      reviewers: selectedReviewers.value,
      reason: reviewReason.value
    }
    if (imageItems.value.length > 0) {
      payload.image_ids = imageItems.value.map((img: any) => img.image_id).filter(Boolean)
    }
    await publisher.dispatchAnnual(payload)
    snackbar.showMessage('已提交人工审核任务，请等待审核', 'success')
    showReviewDialog.value = false
    router.push('/annual')
  } catch (error: any) {
    console.error('Review submit error:', JSON.stringify(error?.response, null, 2))
    const respData = error?.response?.data
    let backendMsg = ''
    if (typeof respData === 'string') {
      backendMsg = respData.substring(0, 200)
    } else if (respData) {
      backendMsg = respData.error || respData.错误 || respData.detail || respData.message || ''
    }
    let message = '提交人工审核任务失败'
    if (error?.code === 'ERR_NETWORK') {
      message = '用户无权限'
    } else if (backendMsg) {
      message = typeof backendMsg === 'string' ? backendMsg : JSON.stringify(backendMsg)
    }
    snackbar.showMessage(message, 'error')
  } finally {
    submittingReview.value = false
  }
}

// --- Data loading ---
const loading = ref(true)

watch(activeTab, () => {
  urn.value.forEach(dimension => {
    dimension.visible = false
  })
  isOverlayVisible.value = false
  activeOverlay.value = ''
})

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

    <!-- ========== Validation Info ========== -->
    <v-row v-if="validation">
      <v-col cols="12">
        <v-alert
          :type="validation.valid !== false ? 'success' : 'warning'"
          variant="tonal"
          class="mb-6"
          rounded="lg"
        >
          <div class="d-flex align-center mb-2">
            <v-icon :color="validation.valid !== false ? 'success' : 'warning'" class="mr-2">
              {{ validation.valid !== false ? 'mdi-check-decagram' : 'mdi-alert-decagram' }}
            </v-icon>
            <span class="text-subtitle-1 font-weight-bold">
              {{ validation.valid !== false ? '材料验证通过' : '材料验证未通过' }}
            </span>
          </div>
          <div v-if="validation.message" class="text-body-2 mb-2">{{ validation.message }}</div>
          <div class="d-flex flex-wrap gap-2">
            <v-chip
              v-for="mt in (validation.material_types_present || [])"
              :key="mt"
              size="small"
              color="success"
              variant="outlined"
            >
              <v-icon start size="x-small">mdi-check</v-icon>
              {{ mt }}
            </v-chip>
            <v-chip
              v-for="mm in (validation.missing_required || [])"
              :key="mm"
              size="small"
              color="error"
              variant="outlined"
            >
              <v-icon start size="x-small">mdi-close</v-icon>
              {{ mm }}
            </v-chip>
          </div>
        </v-alert>
      </v-col>
    </v-row>

    <!-- ========== Evidence Statistics Card ========== -->
    <v-row v-if="evidence && (evidence.model_dir || evidence.aggregate || evidence.section_count !== undefined)">
      <v-col cols="12">
        <v-card class="mb-6" elevation="2" rounded="lg">
          <v-card-title class="pa-6">
            <v-icon color="info" class="mr-2">mdi-chart-bar</v-icon>
            <span class="text-h6">检测统计信息</span>
          </v-card-title>
          <v-card-text class="pa-6">
            <v-row>
              <v-col v-if="evidence.model_dir" cols="12" sm="6" md="3">
                <v-card variant="outlined" rounded="lg" class="pa-3 text-center">
                  <div class="text-caption text-grey mb-1">检测模型</div>
                  <div class="text-body-2 font-weight-medium">{{ evidence.model_dir }}</div>
                </v-card>
              </v-col>
              <v-col v-if="evidence.lang" cols="12" sm="6" md="3">
                <v-card variant="outlined" rounded="lg" class="pa-3 text-center">
                  <div class="text-caption text-grey mb-1">检测语言</div>
                  <div class="text-body-2 font-weight-medium">{{ evidence.lang }}</div>
                </v-card>
              </v-col>
              <v-col v-if="evidence.section_count !== undefined" cols="12" sm="6" md="3">
                <v-card variant="outlined" rounded="lg" class="pa-3 text-center">
                  <div class="text-caption text-grey mb-1">总段落数</div>
                  <div class="text-h5 primary--text">{{ evidence.section_count }}</div>
                </v-card>
              </v-col>
              <v-col v-if="evidence.aigc_section_count !== undefined" cols="12" sm="6" md="3">
                <v-card variant="outlined" rounded="lg" class="pa-3 text-center">
                  <div class="text-caption text-grey mb-1">AIGC段落数</div>
                  <div class="text-h5" :class="evidence.aigc_section_count > 0 ? 'error--text' : 'success--text'">{{ evidence.aigc_section_count }}</div>
                </v-card>
              </v-col>
            </v-row>
            <v-row v-if="evidence.aggregate" class="mt-2">
              <v-col v-if="evidence.aggregate.aigc_ratio !== undefined" cols="12" sm="6" md="3">
                <v-card variant="outlined" rounded="lg" class="pa-3 text-center">
                  <div class="text-caption text-grey mb-1">AIGC比例</div>
                  <div class="text-h5" :class="getProbabilityColor(evidence.aggregate.aigc_ratio) + '--text'">
                    {{ (evidence.aggregate.aigc_ratio * 100).toFixed(1) }}%
                  </div>
                </v-card>
              </v-col>
              <v-col v-if="evidence.aggregate.mean_aigc_probability !== undefined" cols="12" sm="6" md="3">
                <v-card variant="outlined" rounded="lg" class="pa-3 text-center">
                  <div class="text-caption text-grey mb-1">平均AIGC概率</div>
                  <div class="text-h5" :class="getProbabilityColor(evidence.aggregate.mean_aigc_probability) + '--text'">
                    {{ (evidence.aggregate.mean_aigc_probability * 100).toFixed(1) }}%
                  </div>
                </v-card>
              </v-col>
              <v-col v-if="evidence.aggregate.mean_confidence !== undefined" cols="12" sm="6" md="3">
                <v-card variant="outlined" rounded="lg" class="pa-3 text-center">
                  <div class="text-caption text-grey mb-1">平均置信度</div>
                  <div class="text-h5 info--text">{{ (evidence.aggregate.mean_confidence * 100).toFixed(1) }}%</div>
                </v-card>
              </v-col>
              <v-col v-if="evidence.aggregate.max_confidence !== undefined || evidence.aggregate.min_confidence !== undefined" cols="12" sm="6" md="3">
                <v-card variant="outlined" rounded="lg" class="pa-3 text-center">
                  <div class="text-caption text-grey mb-1">置信度范围</div>
                  <div class="text-body-2 font-weight-medium">
                    <span v-if="evidence.aggregate.min_confidence !== undefined">{{ (evidence.aggregate.min_confidence * 100).toFixed(1) }}%</span>
                    <span v-if="evidence.aggregate.min_confidence !== undefined && evidence.aggregate.max_confidence !== undefined"> ~ </span>
                    <span v-if="evidence.aggregate.max_confidence !== undefined">{{ (evidence.aggregate.max_confidence * 100).toFixed(1) }}%</span>
                  </div>
                </v-card>
              </v-col>
            </v-row>
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
          <div v-if="card.files && card.files.length > 0" class="text-left mt-3">
            <div class="text-caption text-grey mb-1">包含文件：</div>
            <div v-for="(file, fi) in card.files" :key="fi" class="d-flex align-center mb-1">
              <v-icon size="x-small" color="grey" class="mr-1">mdi-file-outline</v-icon>
              <span class="text-caption text-truncate">{{ file.file_name || file.name || file }}</span>
            </div>
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

              <!-- Paragraph list: left-right split -->
              <div v-if="paperParagraphs.length > 0">
                <div class="d-flex align-center mb-3">
                  <span class="text-subtitle-1 font-weight-bold">段落AI生成分析</span>
                  <v-spacer />
                  <v-btn-toggle v-model="paperSortMode" mandatory density="compact" variant="outlined" divided>
                    <v-btn value="order" size="small">按顺序</v-btn>
                    <v-btn value="risk" size="small">按风险</v-btn>
                  </v-btn-toggle>
                </div>
                <v-row>
                  <!-- Left: paragraph list -->
                  <v-col cols="12" md="5">
                    <v-card variant="outlined" rounded="lg" class="section-list-card">
                      <div class="section-list-container">
                        <div
                          v-for="para in sortedPaperParagraphs"
                          :key="para.id"
                          class="section-list-item"
                          :class="{ 'section-selected': selectedPaperId === para.id }"
                          @click="selectPaperParagraph(para.id)"
                        >
                          <div class="d-flex align-center mb-1">
                            <v-icon :color="getProbabilityColor(para.confidence)" class="mr-2" size="small">
                              {{ para.confidence > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                            </v-icon>
                            <span class="text-body-2 font-weight-medium text-truncate flex-grow-1">
                              {{ para.title || para.id }}
                            </span>
                            <v-chip :color="getProbabilityColor(para.aigcProb)" size="x-small" class="ml-1">
                              {{ (para.aigcProb * 100).toFixed(0) }}%
                            </v-chip>
                          </div>
                          <div v-if="para.sourceFile" class="text-caption text-grey text-truncate ml-6">
                            {{ para.sourceFile }}
                            <span v-if="para.pageNumber !== null"> · 第{{ para.pageNumber }}页</span>
                          </div>
                          <v-progress-linear :model-value="para.aigcProb * 100" :color="getProbabilityColor(para.aigcProb)" height="2" rounded class="mt-1" />
                        </div>
                      </div>
                    </v-card>
                  </v-col>
                  <!-- Right: detail panel -->
                  <v-col cols="12" md="7">
                    <template v-if="!selectedPaperParagraph">
                      <v-card variant="outlined" rounded="lg" class="pa-8 text-center">
                        <v-icon size="64" color="grey">mdi-cursor-default-click</v-icon>
                        <div class="text-h6 text-grey mt-4">点击左侧段落查看详情</div>
                      </v-card>
                    </template>
                    <template v-else>
                      <!-- Detail header -->
                      <v-card variant="outlined" rounded="lg" class="mb-3">
                        <v-card-title class="d-flex align-center flex-wrap ga-2">
                          <v-icon :color="getProbabilityColor(selectedPaperParagraph.confidence)">
                            {{ selectedPaperParagraph.confidence > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                          </v-icon>
                          <span class="text-h6">{{ selectedPaperParagraph.title || selectedPaperParagraph.id }}</span>
                          <v-chip :color="getProbabilityColor(selectedPaperParagraph.confidence)" size="small">
                            {{ getProbabilityLevel(selectedPaperParagraph.confidence) }}
                          </v-chip>
                          <v-chip v-if="selectedPaperParagraph.isAigc" color="error" size="small">
                            <v-icon start size="x-small">mdi-robot</v-icon> AI生成
                          </v-chip>
                          <v-chip v-else color="success" size="small">
                            <v-icon start size="x-small">mdi-account</v-icon> 人类撰写
                          </v-chip>
                        </v-card-title>
                        <v-card-text>
                          <span v-if="selectedPaperParagraph.sourceFile" class="text-body-2 text-grey mr-4">
                            <v-icon size="small" class="mr-1">mdi-file-document</v-icon>{{ selectedPaperParagraph.sourceFile }}
                          </span>
                          <span v-if="selectedPaperParagraph.pageNumber !== null" class="text-body-2 text-grey mr-4">
                            <v-icon size="small" class="mr-1">mdi-book-open-page-variant</v-icon>第 {{ selectedPaperParagraph.pageNumber }} 页
                          </span>
                          <span class="text-caption text-grey">{{ selectedPaperParagraph.id }}</span>
                        </v-card-text>
                      </v-card>
                      <!-- BERT detection result -->
                      <v-card variant="outlined" rounded="lg" class="mb-3 pa-4">
                        <div class="text-subtitle-2 font-weight-bold mb-2">BERT检测结果</div>
                        <div class="mb-2">
                          <div class="text-caption text-grey mb-1">AI生成置信度</div>
                          <v-progress-linear :model-value="selectedPaperParagraph.confidence * 100" :color="getProbabilityColor(selectedPaperParagraph.confidence)" height="24" rounded>
                            <template #default>
                              <span class="text-caption font-weight-bold" style="color: white">{{ (selectedPaperParagraph.confidence * 100).toFixed(1) }}%</span>
                            </template>
                          </v-progress-linear>
                        </div>
                        <v-row dense>
                          <v-col cols="6">
                            <div class="text-caption text-grey mb-1">人类撰写</div>
                            <v-progress-linear :model-value="selectedPaperParagraph.humanProb * 100" color="success" height="12" rounded />
                            <div class="text-caption text-right mt-1">{{ (selectedPaperParagraph.humanProb * 100).toFixed(1) }}%</div>
                          </v-col>
                          <v-col cols="6">
                            <div class="text-caption text-grey mb-1">AI生成</div>
                            <v-progress-linear :model-value="selectedPaperParagraph.aigcProb * 100" color="error" height="12" rounded />
                            <div class="text-caption text-right mt-1">{{ (selectedPaperParagraph.aigcProb * 100).toFixed(1) }}%</div>
                          </v-col>
                        </v-row>
                        <div class="mt-2">
                          <v-chip size="small">{{ selectedPaperParagraph.labelName }}</v-chip>
                        </div>
                      </v-card>
                      <!-- Original text -->
                      <v-card variant="outlined" rounded="lg">
                        <v-card-title class="d-flex align-center">
                          <v-icon color="info" class="mr-2">mdi-text-box</v-icon>
                          <span class="text-subtitle-1">段落内容</span>
                        </v-card-title>
                        <v-card-text>
                          <div v-if="selectedPaperParagraph.text" class="paragraph-detail-text">{{ selectedPaperParagraph.text }}</div>
                          <div v-else class="text-center py-6">
                            <v-icon size="48" color="grey-lighten-1">mdi-text-box-remove-outline</v-icon>
                            <div class="text-body-1 text-grey mt-2">该段落文本内容未保存</div>
                          </div>
                        </v-card-text>
                      </v-card>
                    </template>
                  </v-col>
                </v-row>
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

              <!-- Review paragraphs detail: left-right split -->
              <div v-if="reviewParagraphs.length > 0" class="mt-4">
                <div class="d-flex align-center mb-3">
                  <span class="text-subtitle-1 font-weight-bold">评审文本段落分析</span>
                  <v-spacer />
                  <v-btn-toggle v-model="reviewSortMode" mandatory density="compact" variant="outlined" divided>
                    <v-btn value="order" size="small">按顺序</v-btn>
                    <v-btn value="risk" size="small">按风险</v-btn>
                  </v-btn-toggle>
                </div>
                <v-row>
                  <!-- Left: paragraph list -->
                  <v-col cols="12" md="5">
                    <v-card variant="outlined" rounded="lg" class="section-list-card">
                      <div class="section-list-container">
                        <div
                          v-for="para in sortedReviewParagraphs"
                          :key="para.id"
                          class="section-list-item"
                          :class="{ 'section-selected': selectedReviewId === para.id }"
                          @click="selectReviewParagraph(para.id)"
                        >
                          <div class="d-flex align-center mb-1">
                            <v-icon :color="getProbabilityColor(para.confidence)" class="mr-2" size="small">
                              {{ para.confidence > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                            </v-icon>
                            <span class="text-body-2 font-weight-medium text-truncate flex-grow-1">
                              {{ para.title || para.id }}
                            </span>
                            <v-chip :color="getProbabilityColor(para.aigcProb)" size="x-small" class="ml-1">
                              {{ (para.aigcProb * 100).toFixed(0) }}%
                            </v-chip>
                          </div>
                          <div v-if="para.sourceFile" class="text-caption text-grey text-truncate ml-6">
                            {{ para.sourceFile }}
                            <span v-if="para.pageNumber !== null"> · 第{{ para.pageNumber }}页</span>
                          </div>
                          <v-progress-linear :model-value="para.aigcProb * 100" :color="getProbabilityColor(para.aigcProb)" height="2" rounded class="mt-1" />
                        </div>
                      </div>
                    </v-card>
                  </v-col>
                  <!-- Right: detail panel -->
                  <v-col cols="12" md="7">
                    <template v-if="!selectedReviewParagraph">
                      <v-card variant="outlined" rounded="lg" class="pa-8 text-center">
                        <v-icon size="64" color="grey">mdi-cursor-default-click</v-icon>
                        <div class="text-h6 text-grey mt-4">点击左侧段落查看详情</div>
                      </v-card>
                    </template>
                    <template v-else>
                      <!-- Detail header -->
                      <v-card variant="outlined" rounded="lg" class="mb-3">
                        <v-card-title class="d-flex align-center flex-wrap ga-2">
                          <v-icon :color="getProbabilityColor(selectedReviewParagraph.confidence)">
                            {{ selectedReviewParagraph.confidence > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                          </v-icon>
                          <span class="text-h6">{{ selectedReviewParagraph.title || selectedReviewParagraph.id }}</span>
                          <v-chip :color="getProbabilityColor(selectedReviewParagraph.confidence)" size="small">
                            {{ getProbabilityLevel(selectedReviewParagraph.confidence) }}
                          </v-chip>
                          <v-chip v-if="selectedReviewParagraph.isAigc" color="error" size="small">
                            <v-icon start size="x-small">mdi-robot</v-icon> AI生成
                          </v-chip>
                          <v-chip v-else color="success" size="small">
                            <v-icon start size="x-small">mdi-account</v-icon> 人类撰写
                          </v-chip>
                        </v-card-title>
                        <v-card-text>
                          <span v-if="selectedReviewParagraph.sourceFile" class="text-body-2 text-grey mr-4">
                            <v-icon size="small" class="mr-1">mdi-file-document</v-icon>{{ selectedReviewParagraph.sourceFile }}
                          </span>
                          <span v-if="selectedReviewParagraph.pageNumber !== null" class="text-body-2 text-grey mr-4">
                            <v-icon size="small" class="mr-1">mdi-book-open-page-variant</v-icon>第 {{ selectedReviewParagraph.pageNumber }} 页
                          </span>
                          <span class="text-caption text-grey">{{ selectedReviewParagraph.id }}</span>
                        </v-card-text>
                      </v-card>
                      <!-- BERT detection result -->
                      <v-card variant="outlined" rounded="lg" class="mb-3 pa-4">
                        <div class="text-subtitle-2 font-weight-bold mb-2">BERT检测结果</div>
                        <div class="mb-2">
                          <div class="text-caption text-grey mb-1">AI生成置信度</div>
                          <v-progress-linear :model-value="selectedReviewParagraph.confidence * 100" :color="getProbabilityColor(selectedReviewParagraph.confidence)" height="24" rounded>
                            <template #default>
                              <span class="text-caption font-weight-bold" style="color: white">{{ (selectedReviewParagraph.confidence * 100).toFixed(1) }}%</span>
                            </template>
                          </v-progress-linear>
                        </div>
                        <v-row dense>
                          <v-col cols="6">
                            <div class="text-caption text-grey mb-1">人类撰写</div>
                            <v-progress-linear :model-value="selectedReviewParagraph.humanProb * 100" color="success" height="12" rounded />
                            <div class="text-caption text-right mt-1">{{ (selectedReviewParagraph.humanProb * 100).toFixed(1) }}%</div>
                          </v-col>
                          <v-col cols="6">
                            <div class="text-caption text-grey mb-1">AI生成</div>
                            <v-progress-linear :model-value="selectedReviewParagraph.aigcProb * 100" color="error" height="12" rounded />
                            <div class="text-caption text-right mt-1">{{ (selectedReviewParagraph.aigcProb * 100).toFixed(1) }}%</div>
                          </v-col>
                        </v-row>
                        <div class="mt-2">
                          <v-chip size="small">{{ selectedReviewParagraph.labelName }}</v-chip>
                        </div>
                      </v-card>
                      <!-- Original text -->
                      <v-card variant="outlined" rounded="lg">
                        <v-card-title class="d-flex align-center">
                          <v-icon color="info" class="mr-2">mdi-text-box</v-icon>
                          <span class="text-subtitle-1">段落内容</span>
                        </v-card-title>
                        <v-card-text>
                          <div v-if="selectedReviewParagraph.text" class="paragraph-detail-text">{{ selectedReviewParagraph.text }}</div>
                          <div v-else class="text-center py-6">
                            <v-icon size="48" color="grey-lighten-1">mdi-text-box-remove-outline</v-icon>
                            <div class="text-body-1 text-grey mt-2">该段落文本内容未保存</div>
                          </div>
                        </v-card-text>
                      </v-card>
                    </template>
                  </v-col>
                </v-row>
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
              <div v-if="imageCard && imageCard.summary" class="text-body-1 mb-4">
                {{ imageCard.summary }}
                <template v-if="imageDetectedCount > 0">
                  （已检测 {{ imageDetectedCount }} 张：<span class="text-error">{{ imageFakeCount }} 疑似造假</span>，<span class="text-success">{{ imageNormalCount }} 正常</span>）
                </template>
              </div>

              <!-- Image grid -->
              <div v-if="imageItems.length > 0" class="image-grid-container">
                <div class="d-flex flex-wrap gap-4">
                  <v-card
                    v-for="(img, idx) in imageItems"
                    :key="idx"
                    width="200"
                    elevation="2"
                    rounded="lg"
                    class="overflow-hidden cursor-pointer"
                    :class="{ 'image-card-fake': img.is_fake, 'image-card-normal': img.result_id && !img.is_fake }"
                    hover
                    @click="viewImageDetail(img)"
                  >
                    <v-img
                      v-if="img.image_url || img.url"
                      :src="getImageUrl(img.image_url || img.url)"
                      height="150"
                      cover
                    >
                      <div class="image-verdict-overlay">
                        <v-chip
                          v-if="img.result_id"
                          :color="img.is_fake ? 'error' : 'success'"
                          size="small"
                          class="ma-2"
                        >
                          <v-icon start size="small">{{ img.is_fake ? 'mdi-alert' : 'mdi-check' }}</v-icon>
                          {{ img.is_fake ? '疑似造假' : '正常' }}
                        </v-chip>
                        <v-chip v-else color="grey" size="small" class="ma-2">
                          <v-icon start size="small">mdi-eye</v-icon>
                          预览
                        </v-chip>
                      </div>
                    </v-img>
                    <v-card-text class="pa-2 text-center">
                      <div v-if="img.result_id" class="text-caption">
                        <v-chip
                          :color="getProbabilityColor(img.confidence || 0)"
                          size="small"
                        >
                          {{ ((img.confidence || 0) * 100).toFixed(1) }}%
                        </v-chip>
                      </div>
                      <div v-if="img.sub_methods && img.sub_methods.length > 0" class="d-flex flex-wrap justify-center ga-1 mt-1">
                        <v-chip
                          v-for="sm in img.sub_methods"
                          :key="sm.method"
                          :color="sm.probability > 0.5 ? 'error' : sm.probability > 0.3 ? 'warning' : 'success'"
                          size="x-small"
                          label
                          variant="tonal"
                        >
                          {{ getSubMethodLabel(sm.method) }} {{ (sm.probability * 100).toFixed(0) }}%
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

    <!-- ========== Raw Result JSON ========== -->
    <v-row>
      <v-col cols="12">
        <v-card class="mb-6" elevation="2" rounded="lg">
          <v-card-title class="pa-6 d-flex align-center" @click="showRawJson = !showRawJson" style="cursor: pointer;">
            <v-icon color="grey-darken-2" class="mr-2">mdi-code-json</v-icon>
            <span class="text-h6">模型返回原始数据</span>
            <v-spacer />
            <v-btn :icon="showRawJson ? 'mdi-chevron-up' : 'mdi-chevron-down'" variant="text" size="small" />
          </v-card-title>
          <v-card-text v-if="showRawJson" class="pa-6">
            <div class="d-flex justify-end mb-2">
              <v-btn size="small" variant="outlined" prepend-icon="mdi-content-copy" @click="copyRawJson">
                复制
              </v-btn>
            </div>
            <pre class="raw-json-pre">{{ JSON.stringify(result, null, 2) }}</pre>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Image Detail Dialog ========== -->
    <v-dialog v-model="showImageDetail" max-width="1000">
      <v-card rounded="lg">
        <v-card-title class="pa-6 d-flex">
          <h1 class="text-h5">图片详情</h1>
          <v-spacer />
          <v-btn icon="mdi-close" variant="text" @click="toggleImageDetailClose" />
        </v-card-title>

        <v-card-text class="pa-6">
          <!-- Loading state -->
          <div v-if="imageDetailLoading" class="text-center py-8">
            <v-progress-circular indeterminate color="primary" size="48" class="mb-4" />
            <div class="text-body-1 text-grey">正在加载检测结果...</div>
          </div>

          <!-- No detection result (expected for multi-material) -->
          <div v-else-if="!hasDetectionResult && !imageDetailError" class="text-center py-6">
            <div v-if="selectedImage" class="mb-4">
              <v-img
                :src="getSelectedImageUrl(selectedImage)"
                max-height="500"
                contain
                class="rounded-lg mx-auto"
                style="max-width: 600px"
              />
            </div>
            <v-alert type="info" variant="tonal" class="mt-4 text-left" density="compact">
              该图片暂无伪造检测结果，可能检测过程中未成功完成。
            </v-alert>
          </div>

          <!-- Actual error -->
          <div v-else-if="imageDetailError" class="text-center py-8">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-image-off-outline</v-icon>
            <div class="text-body-1 text-grey mb-2">{{ imageDetailError }}</div>
          </div>

          <!-- Full detection detail -->
          <div v-else>
            <v-alert v-if="detectionStatus === 'failed'" type="warning" variant="tonal" class="mb-4" density="compact">
              该图片的伪造检测未成功完成，以下结果可能不完整。
            </v-alert>
            <v-alert v-else-if="detectionStatus === 'in_progress'" type="info" variant="tonal" class="mb-4" density="compact">
              该图片的伪造检测仍在进行中，以下结果可能不完整。
            </v-alert>
            <v-row>
              <!-- Left: image + overlay -->
              <v-col cols="12" md="6" class="pr-md-6">
                <div class="image-container">
                  <v-img
                    :src="getSelectedImageUrl(selectedImage)"
                    max-height="500"
                    contain
                    class="rounded-lg"
                  />
                  <transition name="fade">
                    <v-img
                      v-if="activeOverlay && isOverlayVisible"
                      :src="activeOverlay"
                      class="rounded-lg overlay-image"
                    />
                  </transition>
                </div>
                <div class="mt-6">
                  <div class="d-flex flex-column gap-2">
                    <div v-if="exif.detection_time" class="info-item d-flex align-center">
                      <v-icon color="grey" class="mr-2">mdi-clock-outline</v-icon>
                      <span class="text-body-1">检测时间：{{ formatDateTime(exif.detection_time) }}</span>
                    </div>
                    <div class="info-item d-flex align-center">
                      <v-icon color="grey" class="mr-2">mdi-pound</v-icon>
                      <span class="text-body-1">图片编号：{{ selectedImage?.image_id }}</span>
                    </div>
                  </div>
                </div>
              </v-col>

              <!-- Right: tabs -->
              <v-col cols="12" md="6" class="pl-md-6">
                <v-tabs v-model="activeTab" color="primary">
                  <v-tab value="analysis" style="font-size: 16px;">大模型</v-tab>
                  <v-tab value="history" style="font-size: 16px;">深度学习</v-tab>
                  <v-tab value="comments" style="font-size: 16px;">传统方法</v-tab>
                </v-tabs>
                <v-divider />

                <v-window v-model="activeTab" class="mt-4">
                  <!-- Tab 1: LLM -->
                  <v-window-item value="analysis">
                    <div class="d-flex align-center justify-space-between mb-4">
                      <div class="text-h6">大模型意见</div>
                      <v-btn
                        v-if="llm_image"
                        size="small"
                        variant="outlined"
                        color="primary"
                        prepend-icon="mdi-eye"
                        @click="isOverlayVisible = !isOverlayVisible; activeOverlay = isOverlayVisible ? resolveImageUrl(llm_image) : ''"
                      >
                        {{ isOverlayVisible ? '隐藏造假区域' : '展示造假区域' }}
                      </v-btn>
                    </div>
                    <v-card>
                      <v-card-text>
                        <div v-if="llm">{{ llm }}</div>
                        <div v-else class="text-center text-grey py-4">暂无大模型分析结果</div>
                      </v-card-text>
                    </v-card>
                  </v-window-item>

                  <!-- Tab 2: Deep Learning -->
                  <v-window-item value="history">
                    <div class="text-h6 mb-4">深度学习模型结果</div>
                    <v-list v-if="urn.length > 0" class="elevation-1 rounded-lg">
                      <template v-for="(dimension, index) in urn" :key="dimension.method">
                        <v-list-item class="py-2 px-3">
                          <div class="d-flex align-center" style="gap: 24px; width: 100%;">
                            <div class="text-body-1 font-weight-medium" style="min-width: 100px;">
                              {{ dimension.method }}
                            </div>
                            <v-progress-circular
                              :model-value="dimension.probability * 100"
                              :color="getProbabilityColor(dimension.probability)"
                              size="40"
                              width="5"
                            >
                              <span class="text-caption">{{ (dimension.probability * 100).toFixed(0) }}%</span>
                            </v-progress-circular>
                            <v-btn
                              size="small"
                              :color="dimension.visible ? 'error' : 'grey'"
                              variant="tonal"
                              @click="toggleOverlay(dimension)"
                              class="ml-4"
                            >
                              <v-icon size="small" :icon="dimension.visible ? 'mdi-eye-off' : 'mdi-eye'" class="mr-1" />
                              {{ dimension.visible ? '隐藏造假区域' : '显示造假区域' }}
                            </v-btn>
                          </div>
                        </v-list-item>
                        <v-divider v-if="index < urn.length - 1" />
                      </template>
                    </v-list>
                    <div v-else class="text-center text-grey py-4">暂无深度学习检测结果</div>
                  </v-window-item>

                  <!-- Tab 3: Traditional / EXIF -->
                  <v-window-item value="comments">
                    <div class="text-h6 mb-4">传统方法结果</div>
                    <v-card class="mb-4" elevation="2">
                      <v-card-text>
                        <v-list-item>
                          <template #prepend>
                            <v-icon :color="exif.photoshop_edited ? 'error' : 'success'" class="mr-3">
                              {{ exif.photoshop_edited ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                            </v-icon>
                          </template>
                          <v-list-item-title>是否经过PS处理</v-list-item-title>
                          <v-list-item-subtitle>
                            <span :class="exif.photoshop_edited ? 'error--text' : 'success--text'">
                              {{ exif.photoshop_edited ? '检测到PS痕迹' : '未检测到PS痕迹' }}
                            </span>
                          </v-list-item-subtitle>
                        </v-list-item>
                        <v-divider class="my-2" />
                        <v-list-item>
                          <template #prepend>
                            <v-icon :color="exif.time_modified ? 'error' : 'success'" class="mr-3">
                              {{ exif.time_modified ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                            </v-icon>
                          </template>
                          <v-list-item-title>是否经过时间修改</v-list-item-title>
                          <v-list-item-subtitle>
                            <span :class="exif.time_modified ? 'error--text' : 'success--text'">
                              {{ exif.time_modified ? '检测到时间篡改' : '未检测到时间修改' }}
                            </span>
                          </v-list-item-subtitle>
                        </v-list-item>
                      </v-card-text>
                    </v-card>
                    <div v-if="ela" class="mt-4">
                      <div class="text-h6 mb-3">ELA 误差分析图</div>
                      <v-card elevation="2" class="pa-2">
                        <v-img :src="ela" max-height="400" contain class="rounded-lg" />
                      </v-card>
                    </div>
                  </v-window-item>
                </v-window>
              </v-col>
            </v-row>
          </div>
        </v-card-text>
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

/* --- Interactive section list --- */
.section-list-card {
  min-height: 300px;
}

.section-list-container {
  max-height: 500px;
  overflow-y: auto;
  padding: 4px;
}

.section-list-item {
  padding: 12px;
  margin-bottom: 4px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.section-list-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
  border-left-color: #1976d2;
}

.section-list-item.section-selected {
  background-color: rgba(25, 118, 210, 0.08);
  border-left-color: #1976d2;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.paragraph-detail-text {
  line-height: 1.8;
  color: #333;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
  max-height: 400px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

/* --- Image section --- */
.image-grid-container {
  width: 100%;
}

.image-card-fake {
  border-left: 4px solid rgb(var(--v-theme-error)) !important;
}

.image-card-normal {
  border-left: 4px solid rgb(var(--v-theme-success)) !important;
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

/* --- Image detail dialog --- */
.image-container {
  position: relative;
  width: 100%;
}

.overlay-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  mix-blend-mode: multiply;
  opacity: 0.7;
  pointer-events: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.cursor-pointer {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cursor-pointer:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.raw-json-pre {
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  padding: 16px;
  background-color: #1e1e1e;
  color: #d4d4d4;
  border-radius: 8px;
  font-family: "Courier New", Courier, monospace;
  font-size: 0.85rem;
  line-height: 1.5;
  max-height: 600px;
  overflow-y: auto;
}
</style>

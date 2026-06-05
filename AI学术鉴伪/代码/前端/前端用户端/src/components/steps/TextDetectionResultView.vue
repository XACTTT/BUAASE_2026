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

const loading = ref(true)
const showRawJson = ref(false)

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

// --- Review submission state ---
const selectedReviewers = ref<number[]>([])
const reviewReason = ref('')
const reviewSearchQuery = ref('')
const submittingReview = ref(false)

// --- Section checkbox selection (for review submission) ---
const selectedSectionIds = ref<Set<string>>(new Set())

function toggleSectionSelection(item_id: string, checked?: boolean | null) {
  const newSet = new Set(selectedSectionIds.value)
  if (typeof checked === 'boolean') {
    if (checked) {
      newSet.add(item_id)
    } else {
      newSet.delete(item_id)
    }
  } else if (newSet.has(item_id)) {
    newSet.delete(item_id)
  } else {
    newSet.add(item_id)
  }
  selectedSectionIds.value = newSet
}

function isSectionSelected(item_id: string): boolean {
  return selectedSectionIds.value.has(item_id)
}

function selectAllSections(type: 'paper' | 'review') {
  const sections = type === 'paper' ? structuredSections.value : structuredReviewSections.value
  const newSet = new Set(selectedSectionIds.value)
  for (const s of sections) {
    newSet.add(s.item_id)
  }
  selectedSectionIds.value = newSet
}

function deselectAllSections(type: 'paper' | 'review') {
  const sections = type === 'paper' ? structuredSections.value : structuredReviewSections.value
  const ids = new Set(sections.map(s => s.item_id))
  const newSet = new Set([...selectedSectionIds.value].filter(id => !ids.has(id)))
  selectedSectionIds.value = newSet
}

const selectedPaperCount = computed(() => {
  const paperIds = new Set(structuredSections.value.map(s => s.item_id))
  return [...selectedSectionIds.value].filter(id => paperIds.has(id)).length
})

const selectedReviewCount = computed(() => {
  const reviewIds = new Set(structuredReviewSections.value.map(s => s.item_id))
  return [...selectedSectionIds.value].filter(id => reviewIds.has(id)).length
})

// Map selected section item_ids to text resource_ids for submission
const selectedResourceIds = computed<number[]>(() => {
  const idSet = new Set<number>()
  // item_id format:
  //   paper:  {detect_type}_paper_{fileIdx}_{secIdx}        -> resource index = parts[2]
  //   review: {detect_type}_review_file_{fileIdx}_{secIdx}  -> resource index = parts[3]
  //           {detect_type}_review_text_{textIdx}            -> resource index = parts[3]
  const paperResources = textList.value.filter(t => t.text_type === 'paper' || t.text_type === 'multi_material')
  const reviewResources = textList.value.filter(t => t.text_type === 'review' || t.text_type === 'multi_material')

  const selectedPaper = structuredSections.value.filter(s => selectedSectionIds.value.has(s.item_id))
  for (const section of selectedPaper) {
    const parts = section.item_id.split('_')
    const resourceIdx = parseInt(parts[2])
    if (!isNaN(resourceIdx) && resourceIdx < paperResources.length) {
      idSet.add(paperResources[resourceIdx].resource_id)
    }
  }

  const selectedReview = structuredReviewSections.value.filter(s => selectedSectionIds.value.has(s.item_id))
  for (const section of selectedReview) {
    const parts = section.item_id.split('_')
    const resourceIdx = parseInt(parts[3])
    if (!isNaN(resourceIdx) && resourceIdx < reviewResources.length) {
      idSet.add(reviewResources[resourceIdx].resource_id)
    }
  }

  return [...idSet]
})

const manualReviewTaskType = computed(() => {
  const rawTaskType = props.taskMeta?.task_type
  if (['paper_text', 'review_text', 'multi_material'].includes(rawTaskType)) {
    return rawTaskType
  }
  const detectType = props.taskMeta?.detect_type
  if (detectType === 'review') return 'review_text'
  if (detectType === 'multi') return 'multi_material'
  return 'paper_text'
})

const selectedManualReviewResources = computed(() => {
  const materials = props.taskMeta?.materials || {}
  const files = Array.isArray(materials.files) ? materials.files : []
  const reviewTexts = Array.isArray(materials.review_texts) ? materials.review_texts : []
  const fileIds = new Set<number>()
  const textIds = new Set<number>()

  const addFileByIndex = (index: number) => {
    const id = Number(files[index]?.id)
    if (Number.isFinite(id) && id > 0) fileIds.add(id)
  }

  const addTextByIndex = (index: number) => {
    const id = Number(reviewTexts[index]?.id)
    if (Number.isFinite(id) && id > 0) textIds.add(id)
  }

  for (const itemId of selectedSectionIds.value) {
    const parts = String(itemId).split('_')
    const paperIndexPos = parts.lastIndexOf('paper')
    if (paperIndexPos >= 0) {
      addFileByIndex(Number(parts[paperIndexPos + 1]))
      continue
    }

    const reviewFilePos = parts.findIndex((part, index) => part === 'review' && parts[index + 1] === 'file')
    if (reviewFilePos >= 0) {
      addFileByIndex(Number(parts[reviewFilePos + 2]))
      continue
    }

    const reviewTextPos = parts.findIndex((part, index) => part === 'review' && parts[index + 1] === 'text')
    if (reviewTextPos >= 0) {
      addTextByIndex(Number(parts[reviewTextPos + 2]))
    }
  }

  if (fileIds.size === 0 && textIds.size === 0) {
    for (const id of selectedResourceIds.value) {
      if (manualReviewTaskType.value === 'review_text' && files.length === 0) {
        textIds.add(id)
      } else {
        fileIds.add(id)
      }
    }
  }

  return {
    file_ids: [...fileIds],
    text_ids: [...textIds],
    selected_section_ids: [...selectedSectionIds.value],
  }
})

const allPaperSelected = computed(() => {
  return structuredSections.value.length > 0 && selectedPaperCount.value === structuredSections.value.length
})

const allReviewSelected = computed(() => {
  return structuredReviewSections.value.length > 0 && selectedReviewCount.value === structuredReviewSections.value.length
})

// --- Structured section selection (paper - for detail viewing) ---
const selectedSectionId = ref<string | null>(null)
const sortMode = ref<'order' | 'risk'>('order')

// --- Structured section selection (review - for detail viewing) ---
const selectedReviewSectionId = ref<string | null>(null)
const reviewSortMode = ref<'order' | 'risk'>('order')

// --- Structured per_section data from taskMeta ---
interface SectionItem {
  item_id: string
  is_aigc: boolean
  label_name: string
  confidence_score: number
  probabilities: { human?: number; aigc?: number }
  text: string
  title: string
  page_number: number | null
  source_file: string
}

const clampProbability = (value: number): number => {
  if (!Number.isFinite(value)) return 0
  return Math.min(1, Math.max(0, value))
}

const getAigcProbability = (section?: SectionItem | null): number => {
  if (!section) return 0
  const aigcProbability = Number(section.probabilities?.aigc)
  if (Number.isFinite(aigcProbability)) {
    return clampProbability(aigcProbability)
  }

  const confidence = Number(section.confidence_score)
  if (!Number.isFinite(confidence)) return 0
  if (section.is_aigc || section.label_name === 'aigc') {
    return clampProbability(confidence)
  }
  return clampProbability(1 - confidence)
}

const getPredictionConfidence = (section?: SectionItem | null): number => {
  if (!section) return 0
  const confidence = Number(section.confidence_score)
  if (Number.isFinite(confidence)) {
    return clampProbability(confidence)
  }
  return Math.max(
    clampProbability(Number(section.probabilities?.human)),
    clampProbability(Number(section.probabilities?.aigc))
  )
}

const getModelLabel = (section?: SectionItem | null): string => {
  if (!section) return '未知'
  if (section.is_aigc || section.label_name === 'aigc') return 'AI生成'
  if (section.label_name === 'human') return '人类撰写'
  return section.label_name || '未知'
}

const getPredictionConfidenceLabel = (section?: SectionItem | null): string => {
  return getModelLabel(section) === 'AI生成' ? 'AI生成判定置信度' : '人类撰写判定置信度'
}

const formatProbability = (value: number, digits = 1): string => {
  return `${(clampProbability(value) * 100).toFixed(digits)}%`
}

const structuredSections = computed<SectionItem[]>(() => {
  const sections = props.taskMeta?.result?.evidence?.per_section
  if (!Array.isArray(sections)) return []
  return sections.filter((s: any) => s.item_id && s.item_id.includes('_paper_'))
})

const sortedSections = computed(() => {
  if (sortMode.value === 'risk') {
    return [...structuredSections.value].sort((a, b) => getAigcProbability(b) - getAigcProbability(a))
  }
  return structuredSections.value
})

const selectedSection = computed(() => {
  if (!selectedSectionId.value) return null
  return structuredSections.value.find(s => s.item_id === selectedSectionId.value) || null
})

function selectSection(item_id: string) {
  selectedSectionId.value = selectedSectionId.value === item_id ? null : item_id
}

const structuredReviewSections = computed<SectionItem[]>(() => {
  const sections = props.taskMeta?.result?.evidence?.per_section
  if (!Array.isArray(sections)) return []
  return sections.filter((s: any) => s.item_id && s.item_id.includes('_review_'))
})

const sortedReviewSections = computed(() => {
  if (reviewSortMode.value === 'risk') {
    return [...structuredReviewSections.value].sort((a, b) => getAigcProbability(b) - getAigcProbability(a))
  }
  return structuredReviewSections.value
})

const selectedReviewSection = computed(() => {
  if (!selectedReviewSectionId.value) return null
  return structuredReviewSections.value.find(s => s.item_id === selectedReviewSectionId.value) || null
})

function selectReviewSection(item_id: string) {
  selectedReviewSectionId.value = selectedReviewSectionId.value === item_id ? null : item_id
}

const reviewStatistics = computed(() => {
  const sections = structuredReviewSections.value
  let total = sections.length
  let high = 0
  let medium = 0
  let low = 0
  for (const s of sections) {
    const score = getAigcProbability(s)
    if (score > 0.8) high++
    else if (score > 0.5) medium++
    else low++
  }
  return { total, high, medium, low }
})

// --- Paragraph detail dialog (for TOP5 clicks) ---
const showParagraphDialog = ref(false)
const selectedParagraph = ref<SectionItem | null>(null)

function showParagraphDetail(section: SectionItem) {
  selectedParagraph.value = section
  showParagraphDialog.value = true
}

// --- Computed ---
const taskType = computed(() => {
  return props.taskMeta?.task_type || props.taskMeta?.detect_type || ''
})

const hasPaperResults = computed(() => {
  return structuredSections.value.length > 0
})

const hasReviewResults = computed(() => {
  return structuredReviewSections.value.length > 0 || textList.value.some(item => item.text_type === 'review')
})

const paperResults = computed(() => {
  return textList.value.filter(item => item.text_type === 'paper')
})

const reviewResults = computed(() => {
  return textList.value.filter(item => item.text_type === 'review')
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
      metricLabel: 'AI生成概率',
      color: isFake ? 'error' : 'success',
      label: isFake ? '检测到AI生成内容' : '未检测到AI生成内容'
    }
  }
  return null
})

// --- Paper statistics (from structured sections) ---
const paperStatistics = computed(() => {
  const sections = structuredSections.value
  let total = sections.length
  let high = 0
  let medium = 0
  let low = 0
  for (const s of sections) {
    const score = getAigcProbability(s)
    if (score > 0.8) high++
    else if (score > 0.5) medium++
    else low++
  }
  return { total, high, medium, low }
})

// Top 5 high risk sections
const topRiskSections = computed(() => {
  return [...structuredSections.value]
    .sort((a, b) => getAigcProbability(b) - getAigcProbability(a))
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
  // For structured tasks, template data comes from textDetails (fetched per resource)
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
  // Fallback: for structured tasks where textDetails is empty,
  // extract template tendency from dimensions array in taskMeta
  if (data.length === 0 && reviewResults.value.length > 0) {
    const dims = props.taskMeta?.result?.dimensions || props.taskMeta?.dimensions || []
    const templateDim = dims.find((d: any) => d.name === 'template_tendency')
    if (templateDim && templateDim.score !== undefined) {
      data.push({
        score: templateDim.score,
        reason: templateDim.summary || '',
        resource_id: reviewResults.value[0]?.resource_id || 0
      })
    }
  }
  return data
})

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

type DimensionDirection = 'risk' | 'consistency' | 'neutral'

interface DimensionMeta {
  title: string
  metricLabel: string
  description: string
  direction: DimensionDirection
  icon: string
}

const dimensionMetaMap: Record<string, DimensionMeta> = {
  academic_misconduct: {
    title: '学术不端线索',
    metricLabel: '风险指数',
    description: '基于规则提取的抄袭、异常引用等学术不端线索综合估计。',
    direction: 'risk',
    icon: 'mdi-school-outline'
  },
  aigc_generation: {
    title: 'AI生成倾向',
    metricLabel: 'AI生成概率',
    description: '模型对文本由AI生成可能性的综合估计，数值越高越需要关注。',
    direction: 'risk',
    icon: 'mdi-robot-outline'
  },
  section_consistency: {
    title: '段落判定一致性',
    metricLabel: '一致性',
    description: '衡量各段落模型判定是否集中。数值高表示结果更稳定，不代表风险更高。',
    direction: 'consistency',
    icon: 'mdi-vector-combine'
  },
  cross_text_consistency: {
    title: '评审文本判定一致性',
    metricLabel: '一致性',
    description: '衡量多份评审文本检测结果是否集中。数值高表示结果更稳定，不代表风险更高。',
    direction: 'consistency',
    icon: 'mdi-vector-combine'
  },
  cross_material_consistency: {
    title: '材料间判定一致性',
    metricLabel: '一致性',
    description: '衡量论文与评审材料之间的检测结果是否集中。数值高表示结果更稳定，不代表风险更高。',
    direction: 'consistency',
    icon: 'mdi-vector-link'
  },
  aigc_section_ratio: {
    title: 'AI生成段落占比',
    metricLabel: '占比',
    description: '被判为AI生成的段落在全文中的占比，数值越高说明涉及范围越大。',
    direction: 'risk',
    icon: 'mdi-chart-pie'
  },
  aigc_ratio: {
    title: 'AI生成文本占比',
    metricLabel: '占比',
    description: '被判为AI生成的文本在全部材料中的占比，数值越高说明涉及范围越大。',
    direction: 'risk',
    icon: 'mdi-chart-pie'
  },
  max_section_risk: {
    title: '最高单段风险',
    metricLabel: '最高AI生成概率',
    description: '单个段落中出现的最高AI生成概率，用于提示最需要复核的位置。',
    direction: 'risk',
    icon: 'mdi-alert-decagram-outline'
  },
  max_risk: {
    title: '最高文本风险',
    metricLabel: '最高AI生成概率',
    description: '全部材料中出现的最高AI生成概率，用于提示最需要复核的位置。',
    direction: 'risk',
    icon: 'mdi-alert-decagram-outline'
  },
  peak_risk: {
    title: '最高单文本风险',
    metricLabel: '最高AI生成概率',
    description: '单份评审文本中出现的最高AI生成概率，用于提示最需要复核的位置。',
    direction: 'risk',
    icon: 'mdi-alert-decagram-outline'
  },
  template_tendency: {
    title: '模板化倾向',
    metricLabel: '模板化指数',
    description: '衡量评审文本套话或模板化表达的倾向，数值越高越需要关注。',
    direction: 'risk',
    icon: 'mdi-text-box-search-outline'
  },
  text_tampering: {
    title: '文本篡改线索',
    metricLabel: '风险指数',
    description: '基于文本结构和内容异常提取的篡改线索综合估计。',
    direction: 'risk',
    icon: 'mdi-file-edit-outline'
  },
  data_chart_fabrication_hint: {
    title: '数据图表异常线索',
    metricLabel: '风险指数',
    description: '基于数值、图表和文本一致性线索估计的数据图表异常风险。',
    direction: 'risk',
    icon: 'mdi-chart-line-variant'
  }
}

// Evidence
const evidence = computed(() => {
  return props.taskMeta?.result?.evidence || null
})

interface RiskStats {
  total: number
  high: number
  medium: number
  low: number
}

function getRiskDistributionItems(stats: RiskStats) {
  const total = stats.total || 0
  return [
    {
      key: 'high',
      label: '高风险段落',
      count: stats.high || 0,
      percent: total > 0 ? ((stats.high || 0) / total) * 100 : 0,
      color: 'error',
      note: 'AI生成概率高于 80%'
    },
    {
      key: 'medium',
      label: '中风险段落',
      count: stats.medium || 0,
      percent: total > 0 ? ((stats.medium || 0) / total) * 100 : 0,
      color: 'warning',
      note: 'AI生成概率介于 50% 到 80%'
    },
    {
      key: 'low',
      label: '低风险段落',
      count: stats.low || 0,
      percent: total > 0 ? ((stats.low || 0) / total) * 100 : 0,
      color: 'success',
      note: 'AI生成概率不高于 50%'
    }
  ]
}

function getDimensionMeta(dim: any, index: number): DimensionMeta {
  const name = String(dim?.name || '')
  return dimensionMetaMap[name] || {
    title: `检测指标 ${index + 1}`,
    metricLabel: '指标值',
    description: '模型返回的辅助检测指标，请结合段落明细一并判断。',
    direction: 'neutral',
    icon: 'mdi-chart-box-outline'
  }
}

function getDimensionScore(dim: any): number {
  return clampProbability(Number(dim?.score))
}

function getDimensionLevel(dim: any, index: number) {
  const score = getDimensionScore(dim)
  const meta = getDimensionMeta(dim, index)

  if (meta.direction === 'consistency') {
    if (score >= 0.7) return { text: '结果较稳定', color: 'info', icon: 'mdi-check-circle-outline' }
    if (score >= 0.4) return { text: '存在一定分歧', color: 'warning', icon: 'mdi-alert-outline' }
    return { text: '分歧较大', color: 'warning', icon: 'mdi-alert-circle-outline' }
  }

  if (meta.direction === 'risk') {
    if (score > 0.8) return { text: '高风险', color: 'error', icon: 'mdi-alert-octagon-outline' }
    if (score > 0.5) return { text: '中风险', color: 'warning', icon: 'mdi-alert-outline' }
    return { text: '风险较低', color: 'success', icon: 'mdi-check-circle-outline' }
  }

  return { text: '参考指标', color: 'primary', icon: 'mdi-information-outline' }
}

function formatDimensionScore(dim: any): string {
  if (dim?.score === undefined || dim?.score === null) return '暂无数据'
  return formatProbability(getDimensionScore(dim))
}

function getDimensionSummary(dim: any, index: number): string {
  const meta = getDimensionMeta(dim, index)
  return meta.description || dim?.summary || '模型返回的辅助检测指标，请结合段落明细一并判断。'
}

// Review submission
const canSubmitReview = computed(() => {
  return selectedSectionIds.value.size > 0 && selectedReviewers.value.length > 0
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

function clearReviewSelection() {
  selectedSectionIds.value = new Set()
  selectedReviewers.value = []
  reviewReason.value = ''
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
    const selectedResources = selectedManualReviewResources.value
    const payload: any = {
      task_id: props.taskId,
      task_type: manualReviewTaskType.value,
      review_type: 'text',
      file_ids: selectedResources.file_ids,
      text_ids: selectedResources.text_ids,
      selected_section_ids: selectedResources.selected_section_ids,
      reviewers: selectedReviewers.value,
      reason: reviewReason.value
    }
    await publisher.dispatchAnnual(payload)
    snackbar.showMessage('已提交人工审核任务，请等待审核', 'success')
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
    if (error?.response?.status === 403) {
      message = backendMsg || '该用户没有发布的权限'
    } else if (error?.code === 'ERR_NETWORK') {
      message = '网络错误，请检查连接'
    } else if (backendMsg) {
      message = typeof backendMsg === 'string' ? backendMsg : JSON.stringify(backendMsg)
    }
    snackbar.showMessage(message, 'error')
  } finally {
    submittingReview.value = false
  }
}

const copyRawJson = () => {
  const text = JSON.stringify(props.taskMeta, null, 2)
  navigator.clipboard.writeText(text).then(() => {
    snackbar.showMessage('已复制到剪贴板', 'success')
  }).catch(() => {
    snackbar.showMessage('复制失败', 'error')
  })
}

// --- Data loading ---
onMounted(async () => {
  loading.value = true
  try {
    // Fetch text results list (still needed for review text section)
    const textListResp = await publisher.getTaskTextResults(props.taskId)
    const results = textListResp.data?.results || []
    textList.value = results

    // Fetch detail for each result (needed for review text details)
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
                      {{ overallConclusion.metricLabel }}
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
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- ========== Paper Text Section (Redesigned) ========== -->
    <template v-if="hasPaperResults">
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

      <!-- Combined Risk Distribution + Dimensions Card -->
      <v-card class="mb-6" elevation="2" rounded="lg">
        <v-card-title class="pa-6 pb-4">
          <div class="d-flex align-center flex-wrap gap-2">
            <v-icon color="primary" class="mr-2">mdi-chart-box</v-icon>
            <span class="text-h6">风险分析与维度评估</span>
            <v-chip color="primary" size="small" variant="tonal">AI生成概率口径</v-chip>
          </div>
        </v-card-title>
        <v-card-text class="pa-6 pt-0">
          <v-row class="align-stretch">
            <v-col cols="12" md="4">
              <div class="analysis-panel pa-4 rounded-lg h-100">
                <div class="d-flex align-center justify-space-between mb-2">
                  <div class="text-subtitle-2 font-weight-bold">风险分布</div>
                  <v-chip size="small" color="primary" variant="tonal">{{ paperStatistics.total }} 段</v-chip>
                </div>
                <div class="text-caption text-grey mb-4">
                  按段落 AI 生成概率分层，红色表示需要重点复核，绿色表示当前风险较低。
                </div>
                <template v-if="paperStatistics.total > 0">
                  <div
                    v-for="item in getRiskDistributionItems(paperStatistics)"
                    :key="item.key"
                    class="risk-distribution-row"
                  >
                    <div class="d-flex justify-space-between align-center gap-2">
                      <span class="text-body-2 font-weight-medium">{{ item.label }}</span>
                      <span class="text-body-2 font-weight-bold">{{ item.count }} 段 · {{ item.percent.toFixed(0) }}%</span>
                    </div>
                    <v-progress-linear
                      :model-value="item.percent"
                      :color="item.color"
                      height="10"
                      rounded
                      class="my-2"
                    />
                    <div class="text-caption text-grey">{{ item.note }}</div>
                  </div>
                </template>
                <div v-else class="text-center text-grey py-4">
                  暂无风险分布数据
                </div>
              </div>
            </v-col>
            <v-col cols="12" md="8" v-if="dimensions && Array.isArray(dimensions) && dimensions.length > 0">
              <div class="d-flex align-center justify-space-between mb-4">
                <div class="text-subtitle-2 font-weight-bold">检测维度</div>
                <div class="text-caption text-grey">指标值不等同于风险结论，请看右侧状态标签</div>
              </div>
              <v-row>
                <v-col
                  v-for="(dim, idx) in dimensions"
                  :key="idx"
                  cols="12"
                  sm="6"
                >
                  <v-card variant="outlined" rounded="lg" class="dimension-card pa-4 h-100">
                    <div class="d-flex align-start justify-space-between gap-3 mb-3">
                      <div class="d-flex align-start" style="min-width: 0;">
                        <v-icon :color="getDimensionLevel(dim, idx).color" size="22" class="mr-2 mt-1">
                          {{ getDimensionMeta(dim, idx).icon }}
                        </v-icon>
                        <div style="min-width: 0;">
                          <div class="text-subtitle-1 font-weight-bold">{{ getDimensionMeta(dim, idx).title }}</div>
                          <div class="text-caption text-grey">{{ getDimensionMeta(dim, idx).metricLabel }}</div>
                        </div>
                      </div>
                      <v-chip
                        :color="getDimensionLevel(dim, idx).color"
                        size="small"
                        variant="tonal"
                        class="flex-shrink-0"
                      >
                        <v-icon start size="x-small">{{ getDimensionLevel(dim, idx).icon }}</v-icon>
                        {{ getDimensionLevel(dim, idx).text }}
                      </v-chip>
                    </div>
                    <div class="dimension-score-row mb-2">
                      <span class="dimension-score">{{ formatDimensionScore(dim) }}</span>
                    </div>
                    <v-progress-linear
                      :model-value="getDimensionScore(dim) * 100"
                      :color="getDimensionLevel(dim, idx).color"
                      height="8"
                      rounded
                      class="mb-3"
                    />
                    <div class="text-body-2 text-grey">{{ getDimensionSummary(dim, idx) }}</div>
                  </v-card>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Paper content: Left section list + Right detail panel -->
      <v-row>
        <!-- Left Column: Section List -->
        <v-col cols="12" md="4">
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="d-flex justify-space-between align-center pa-6">
              <div class="d-flex align-center">
                <v-icon color="primary" class="mr-2">mdi-format-list-bulleted</v-icon>
                <span class="text-h6">段落列表</span>
              </div>
              <div class="d-flex align-center gap-2">
                <v-chip size="small" color="primary" variant="tonal">
                  {{ selectedPaperCount }}/{{ structuredSections.length }}
                </v-chip>
                <v-btn
                  v-if="!allPaperSelected"
                  size="x-small"
                  variant="text"
                  color="primary"
                  @click="selectAllSections('paper')"
                >
                  全选
                </v-btn>
                <v-btn
                  v-else
                  size="x-small"
                  variant="text"
                  color="error"
                  @click="deselectAllSections('paper')"
                >
                  取消全选
                </v-btn>
              </div>
            </v-card-title>
            <v-card-text class="pa-4 pt-0">
              <div v-if="structuredSections.length === 0" class="text-center text-grey py-8">
                暂无段落分析数据
              </div>
              <div v-else>
                <!-- Sort toggle -->
                <v-btn-toggle
                  v-model="sortMode"
                  mandatory
                  density="compact"
                  variant="outlined"
                  divided
                  class="mb-3 w-100"
                >
                  <v-btn value="order" size="small" class="flex-grow-1">
                    <v-icon start size="small">mdi-sort-ascending</v-icon>
                    按顺序排列
                  </v-btn>
                  <v-btn value="risk" size="small" class="flex-grow-1">
                    <v-icon start size="small">mdi-sort-alert</v-icon>
                    按风险排列
                  </v-btn>
                </v-btn-toggle>
                <div class="section-list-container">
                <div
                  v-for="section in sortedSections"
                  :key="section.item_id"
                  class="section-list-item pa-3 mb-2 rounded-lg cursor-pointer"
                  :class="{
                    'section-selected': selectedSectionId === section.item_id,
                    'section-checked': isSectionSelected(section.item_id)
                  }"
                  @click="selectSection(section.item_id)"
                >
                  <div class="d-flex align-center justify-space-between">
                    <div class="d-flex align-center" style="min-width: 0; flex: 1;">
                      <v-checkbox
                        :model-value="isSectionSelected(section.item_id)"
                        @click.stop
                        @update:model-value="(checked) => toggleSectionSelection(section.item_id, checked)"
                        color="primary"
                        hide-details
                        density="compact"
                        class="flex-shrink-0 mr-1"
                        style="margin-top: 0; padding-top: 0;"
                      />
                      <v-icon
                        :color="getProbabilityColor(getAigcProbability(section))"
                        size="small"
                        class="mr-2 flex-shrink-0"
                      >
                        {{ getAigcProbability(section) > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                      </v-icon>
                      <div style="min-width: 0; flex: 1;">
                        <div class="text-body-2 font-weight-medium text-truncate">
                          {{ section.title || section.item_id }}
                        </div>
                        <div v-if="section.source_file" class="text-caption text-grey text-truncate">
                          {{ section.source_file }}
                          <span v-if="section.page_number !== null && section.page_number !== undefined">
                            · 第{{ (section.page_number + 1) }}页
                          </span>
                        </div>
                      </div>
                    </div>
                    <v-chip
                      :color="getProbabilityColor(getAigcProbability(section))"
                      size="x-small"
                      class="ml-2 flex-shrink-0"
                    >
                      {{ formatProbability(getAigcProbability(section), 0) }}
                    </v-chip>
                  </div>
                  <!-- Mini progress bar -->
                  <v-progress-linear
                    :model-value="getAigcProbability(section) * 100"
                    :color="getProbabilityColor(getAigcProbability(section))"
                    height="3"
                    rounded
                    class="mt-2"
                  />
                </div>
              </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Right Column: Section Detail Panel -->
        <v-col cols="12" md="8">
          <!-- No section selected placeholder -->
          <v-card v-if="!selectedSection" elevation="2" rounded="lg" class="pa-8 text-center">
            <v-icon size="64" color="grey">mdi-cursor-default-click</v-icon>
            <div class="text-h6 text-grey mt-4">点击左侧段落查看详情</div>
            <div class="text-body-2 text-grey mt-2">选择任意段落查看完整的检测分析结果</div>
          </v-card>

          <!-- Selected section detail -->
          <template v-else>
            <!-- Section header card -->
            <v-card class="mb-6" elevation="2" rounded="lg">
              <v-card-title class="pa-6">
                <div class="d-flex align-center flex-wrap gap-2">
                  <v-icon :color="getProbabilityColor(getAigcProbability(selectedSection))" class="mr-1">
                    {{ getAigcProbability(selectedSection) > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                  </v-icon>
                  <span class="text-h6">{{ selectedSection.title || selectedSection.item_id }}</span>
                  <v-chip :color="getProbabilityColor(getAigcProbability(selectedSection))" size="small">
                    {{ getProbabilityLevel(getAigcProbability(selectedSection)) }}
                  </v-chip>
                  <v-chip v-if="selectedSection.is_aigc" color="error" size="small" variant="tonal">
                    <v-icon start size="x-small">mdi-robot</v-icon>
                    AI生成
                  </v-chip>
                  <v-chip v-else color="success" size="small" variant="tonal">
                    <v-icon start size="x-small">mdi-account</v-icon>
                    人类撰写
                  </v-chip>
                </div>
              </v-card-title>
              <v-card-text class="pa-6 pt-0">
                <div class="d-flex flex-wrap gap-3 text-body-2 text-grey">
                  <span v-if="selectedSection.source_file">
                    <v-icon size="small" class="mr-1">mdi-file-document</v-icon>
                    {{ selectedSection.source_file }}
                  </span>
                  <span v-if="selectedSection.page_number !== null && selectedSection.page_number !== undefined">
                    <v-icon size="small" class="mr-1">mdi-book-open-page-variant</v-icon>
                    第 {{ (selectedSection.page_number + 1) }} 页
                  </span>
                  <span>
                    <v-icon size="small" class="mr-1">mdi-identifier</v-icon>
                    {{ selectedSection.item_id }}
                  </span>
                </div>
              </v-card-text>
            </v-card>

            <!-- BERT Detection Result Card -->
            <v-card class="mb-6" elevation="2" rounded="lg">
              <v-card-title class="pa-6">
                <v-icon color="primary" class="mr-2">mdi-brain</v-icon>
                <span class="text-h6">BERT 检测结果</span>
              </v-card-title>
              <v-card-text class="pa-6 pt-0">
                <v-row>
                  <v-col cols="12" md="6">
                    <div class="text-subtitle-2 font-weight-bold mb-2">AI生成概率</div>
                    <v-progress-linear
                      :model-value="getAigcProbability(selectedSection) * 100"
                      :color="getProbabilityColor(getAigcProbability(selectedSection))"
                      height="28"
                      rounded
                    >
                      <template #default="{ value }">
                        <strong>{{ value.toFixed(1) }}%</strong>
                      </template>
                    </v-progress-linear>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="text-subtitle-2 font-weight-bold mb-2">概率分布</div>
                    <div class="d-flex align-center gap-4">
                      <div class="flex-grow-1">
                        <div class="text-caption text-grey mb-1">人类撰写</div>
                        <v-progress-linear
                          :model-value="(selectedSection.probabilities?.human || 0) * 100"
                          color="success"
                          height="12"
                          rounded
                        />
                        <div class="text-caption text-right">{{ ((selectedSection.probabilities?.human || 0) * 100).toFixed(1) }}%</div>
                      </div>
                      <div class="flex-grow-1">
                        <div class="text-caption text-grey mb-1">AI生成</div>
                        <v-progress-linear
                          :model-value="(selectedSection.probabilities?.aigc || 0) * 100"
                          color="error"
                          height="12"
                          rounded
                        />
                        <div class="text-caption text-right">{{ ((selectedSection.probabilities?.aigc || 0) * 100).toFixed(1) }}%</div>
                      </div>
                    </div>
                  </v-col>
                </v-row>
                <div v-if="selectedSection.label_name" class="mt-4">
                  <v-chip
                    :color="selectedSection.is_aigc ? 'error' : 'success'"
                    variant="tonal"
                  >
                    模型判定：{{ getModelLabel(selectedSection) }}，{{ getPredictionConfidenceLabel(selectedSection) }} {{ formatProbability(getPredictionConfidence(selectedSection)) }}
                  </v-chip>
                </div>
              </v-card-text>
            </v-card>

            <!-- Section Text Content Card -->
            <v-card class="mb-6" elevation="2" rounded="lg">
              <v-card-title class="pa-6">
                <v-icon color="info" class="mr-2">mdi-text-box</v-icon>
                <span class="text-h6">段落内容</span>
              </v-card-title>
              <v-card-text class="pa-6 pt-0">
                <div v-if="selectedSection.text" class="paragraph-detail-text">{{ selectedSection.text }}</div>
                <div v-else class="text-center py-8">
                  <v-icon size="48" color="grey-lighten-1">mdi-text-box-remove-outline</v-icon>
                  <div class="text-body-1 text-grey mt-2">该段落文本内容未保存</div>
                  <div class="text-caption text-grey mt-1">请重新执行检测以获取完整文本数据</div>
                </div>
              </v-card-text>
            </v-card>
          </template>

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
      </v-row>
    </template>

    <!-- ========== Review Text Section (Redesigned) ========== -->
    <template v-if="hasReviewResults && (taskType === 'review_text' || taskType === 'multi_material')">
      <!-- Review-specific: Template Tendency Analysis -->
      <v-row>
        <!-- Left Column: Gauge + Reasons -->
        <v-col cols="12" md="8">
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

          <!-- Template Analysis Reason Cards (one per review text) -->
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

        <!-- Right Column: Distribution + Quality -->
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

      <!-- LLM Analysis Card -->
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
              <div v-if="typeof llmAnalysis === 'string'" class="text-body-1 analysis-text">
                {{ llmAnalysis }}
              </div>
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

      <!-- Review Statistics Row -->
      <v-row class="mb-6">
        <v-col cols="12" md="3">
          <v-card elevation="2" rounded="lg" class="text-center pa-4">
            <div class="text-h4 primary--text">{{ reviewStatistics.total }}</div>
            <div class="text-body-2 text-grey mt-1">总段落数</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card elevation="2" rounded="lg" class="text-center pa-4" color="red-lighten-5">
            <div class="text-h4 error--text">{{ reviewStatistics.high }}</div>
            <div class="text-body-2 text-grey mt-1">高风险段落</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card elevation="2" rounded="lg" class="text-center pa-4" color="orange-lighten-5">
            <div class="text-h4 warning--text">{{ reviewStatistics.medium }}</div>
            <div class="text-body-2 text-grey mt-1">中风险段落</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card elevation="2" rounded="lg" class="text-center pa-4" color="green-lighten-5">
            <div class="text-h4 success--text">{{ reviewStatistics.low }}</div>
            <div class="text-body-2 text-grey mt-1">低风险段落</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Review: Risk Distribution + Dimensions -->
      <v-card class="mb-6" elevation="2" rounded="lg">
        <v-card-title class="pa-6 pb-4">
          <div class="d-flex align-center flex-wrap gap-2">
            <v-icon color="primary" class="mr-2">mdi-chart-box</v-icon>
            <span class="text-h6">风险分析与维度评估</span>
            <v-chip color="primary" size="small" variant="tonal">AI生成概率口径</v-chip>
          </div>
        </v-card-title>
        <v-card-text class="pa-6 pt-0">
          <v-row class="align-stretch">
            <v-col cols="12" md="4">
              <div class="analysis-panel pa-4 rounded-lg h-100">
                <div class="d-flex align-center justify-space-between mb-2">
                  <div class="text-subtitle-2 font-weight-bold">风险分布</div>
                  <v-chip size="small" color="primary" variant="tonal">{{ reviewStatistics.total }} 段</v-chip>
                </div>
                <div class="text-caption text-grey mb-4">
                  按文本 AI 生成概率分层，红色表示需要重点复核，绿色表示当前风险较低。
                </div>
                <template v-if="reviewStatistics.total > 0">
                  <div
                    v-for="item in getRiskDistributionItems(reviewStatistics)"
                    :key="item.key"
                    class="risk-distribution-row"
                  >
                    <div class="d-flex justify-space-between align-center gap-2">
                      <span class="text-body-2 font-weight-medium">{{ item.label }}</span>
                      <span class="text-body-2 font-weight-bold">{{ item.count }} 段 · {{ item.percent.toFixed(0) }}%</span>
                    </div>
                    <v-progress-linear
                      :model-value="item.percent"
                      :color="item.color"
                      height="10"
                      rounded
                      class="my-2"
                    />
                    <div class="text-caption text-grey">{{ item.note }}</div>
                  </div>
                </template>
                <div v-else class="text-center text-grey py-4">
                  暂无风险分布数据
                </div>
              </div>
            </v-col>
            <v-col cols="12" md="8" v-if="dimensions && Array.isArray(dimensions) && dimensions.length > 0">
              <div class="d-flex align-center justify-space-between mb-4">
                <div class="text-subtitle-2 font-weight-bold">检测维度</div>
                <div class="text-caption text-grey">指标值不等同于风险结论，请看右侧状态标签</div>
              </div>
              <v-row>
                <v-col
                  v-for="(dim, idx) in dimensions"
                  :key="idx"
                  cols="12"
                  sm="6"
                >
                  <v-card variant="outlined" rounded="lg" class="dimension-card pa-4 h-100">
                    <div class="d-flex align-start justify-space-between gap-3 mb-3">
                      <div class="d-flex align-start" style="min-width: 0;">
                        <v-icon :color="getDimensionLevel(dim, idx).color" size="22" class="mr-2 mt-1">
                          {{ getDimensionMeta(dim, idx).icon }}
                        </v-icon>
                        <div style="min-width: 0;">
                          <div class="text-subtitle-1 font-weight-bold">{{ getDimensionMeta(dim, idx).title }}</div>
                          <div class="text-caption text-grey">{{ getDimensionMeta(dim, idx).metricLabel }}</div>
                        </div>
                      </div>
                      <v-chip
                        :color="getDimensionLevel(dim, idx).color"
                        size="small"
                        variant="tonal"
                        class="flex-shrink-0"
                      >
                        <v-icon start size="x-small">{{ getDimensionLevel(dim, idx).icon }}</v-icon>
                        {{ getDimensionLevel(dim, idx).text }}
                      </v-chip>
                    </div>
                    <div class="dimension-score-row mb-2">
                      <span class="dimension-score">{{ formatDimensionScore(dim) }}</span>
                    </div>
                    <v-progress-linear
                      :model-value="getDimensionScore(dim) * 100"
                      :color="getDimensionLevel(dim, idx).color"
                      height="8"
                      rounded
                      class="mb-3"
                    />
                    <div class="text-body-2 text-grey">{{ getDimensionSummary(dim, idx) }}</div>
                  </v-card>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Review content: Left section list + Right detail panel -->
      <v-row>
        <!-- Left Column: Review Section List -->
        <v-col cols="12" md="4">
          <v-card class="mb-6" elevation="2" rounded="lg">
            <v-card-title class="d-flex justify-space-between align-center pa-6">
              <div class="d-flex align-center">
                <v-icon color="primary" class="mr-2">mdi-format-list-bulleted</v-icon>
                <span class="text-h6">段落列表</span>
              </div>
              <div class="d-flex align-center gap-2">
                <v-chip size="small" color="primary" variant="tonal">
                  {{ selectedReviewCount }}/{{ structuredReviewSections.length }}
                </v-chip>
                <v-btn
                  v-if="!allReviewSelected"
                  size="x-small"
                  variant="text"
                  color="primary"
                  @click="selectAllSections('review')"
                >
                  全选
                </v-btn>
                <v-btn
                  v-else
                  size="x-small"
                  variant="text"
                  color="error"
                  @click="deselectAllSections('review')"
                >
                  取消全选
                </v-btn>
              </div>
            </v-card-title>
            <v-card-text class="pa-4 pt-0">
              <div v-if="structuredReviewSections.length === 0" class="text-center text-grey py-8">
                暂无段落分析数据
              </div>
              <div v-else>
                <!-- Sort toggle -->
                <v-btn-toggle
                  v-model="reviewSortMode"
                  mandatory
                  density="compact"
                  variant="outlined"
                  divided
                  class="mb-3 w-100"
                >
                  <v-btn value="order" size="small" class="flex-grow-1">
                    <v-icon start size="small">mdi-sort-ascending</v-icon>
                    按顺序排列
                  </v-btn>
                  <v-btn value="risk" size="small" class="flex-grow-1">
                    <v-icon start size="small">mdi-sort-alert</v-icon>
                    按风险排列
                  </v-btn>
                </v-btn-toggle>
                <div class="section-list-container">
                <div
                  v-for="section in sortedReviewSections"
                  :key="section.item_id"
                  class="section-list-item pa-3 mb-2 rounded-lg cursor-pointer"
                  :class="{
                    'section-selected': selectedReviewSectionId === section.item_id,
                    'section-checked': isSectionSelected(section.item_id)
                  }"
                  @click="selectReviewSection(section.item_id)"
                >
                  <div class="d-flex align-center justify-space-between">
                    <div class="d-flex align-center" style="min-width: 0; flex: 1;">
                      <v-checkbox
                        :model-value="isSectionSelected(section.item_id)"
                        @click.stop
                        @update:model-value="(checked) => toggleSectionSelection(section.item_id, checked)"
                        color="primary"
                        hide-details
                        density="compact"
                        class="flex-shrink-0 mr-1"
                        style="margin-top: 0; padding-top: 0;"
                      />
                      <v-icon
                        :color="getProbabilityColor(getAigcProbability(section))"
                        size="small"
                        class="mr-2 flex-shrink-0"
                      >
                        {{ getAigcProbability(section) > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                      </v-icon>
                      <div style="min-width: 0; flex: 1;">
                        <div class="text-body-2 font-weight-medium text-truncate">
                          {{ section.title || section.item_id }}
                        </div>
                        <div v-if="section.source_file" class="text-caption text-grey text-truncate">
                          {{ section.source_file }}
                          <span v-if="section.page_number !== null && section.page_number !== undefined">
                            · 第{{ (section.page_number + 1) }}页
                          </span>
                        </div>
                      </div>
                    </div>
                    <v-chip
                      :color="getProbabilityColor(getAigcProbability(section))"
                      size="x-small"
                      class="ml-2 flex-shrink-0"
                    >
                      {{ formatProbability(getAigcProbability(section), 0) }}
                    </v-chip>
                  </div>
                  <!-- Mini progress bar -->
                  <v-progress-linear
                    :model-value="getAigcProbability(section) * 100"
                    :color="getProbabilityColor(getAigcProbability(section))"
                    height="3"
                    rounded
                    class="mt-2"
                  />
                </div>
              </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Right Column: Review Section Detail Panel -->
        <v-col cols="12" md="8">
          <!-- No section selected placeholder -->
          <v-card v-if="!selectedReviewSection" elevation="2" rounded="lg" class="pa-8 text-center">
            <v-icon size="64" color="grey">mdi-cursor-default-click</v-icon>
            <div class="text-h6 text-grey mt-4">点击左侧段落查看详情</div>
            <div class="text-body-2 text-grey mt-2">选择任意段落查看完整的检测分析结果</div>
          </v-card>

          <!-- Selected review section detail -->
          <template v-else>
            <!-- Section header card -->
            <v-card class="mb-6" elevation="2" rounded="lg">
              <v-card-title class="pa-6">
                <div class="d-flex align-center flex-wrap gap-2">
                  <v-icon :color="getProbabilityColor(getAigcProbability(selectedReviewSection))" class="mr-1">
                    {{ getAigcProbability(selectedReviewSection) > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                  </v-icon>
                  <span class="text-h6">{{ selectedReviewSection.title || selectedReviewSection.item_id }}</span>
                  <v-chip :color="getProbabilityColor(getAigcProbability(selectedReviewSection))" size="small">
                    {{ getProbabilityLevel(getAigcProbability(selectedReviewSection)) }}
                  </v-chip>
                  <v-chip v-if="selectedReviewSection.is_aigc" color="error" size="small" variant="tonal">
                    <v-icon start size="x-small">mdi-robot</v-icon>
                    AI生成
                  </v-chip>
                  <v-chip v-else color="success" size="small" variant="tonal">
                    <v-icon start size="x-small">mdi-account</v-icon>
                    人类撰写
                  </v-chip>
                </div>
              </v-card-title>
              <v-card-text class="pa-6 pt-0">
                <div class="d-flex flex-wrap gap-3 text-body-2 text-grey">
                  <span v-if="selectedReviewSection.source_file">
                    <v-icon size="small" class="mr-1">mdi-file-document</v-icon>
                    {{ selectedReviewSection.source_file }}
                  </span>
                  <span v-if="selectedReviewSection.page_number !== null && selectedReviewSection.page_number !== undefined">
                    <v-icon size="small" class="mr-1">mdi-book-open-page-variant</v-icon>
                    第 {{ (selectedReviewSection.page_number + 1) }} 页
                  </span>
                  <span>
                    <v-icon size="small" class="mr-1">mdi-identifier</v-icon>
                    {{ selectedReviewSection.item_id }}
                  </span>
                </div>
              </v-card-text>
            </v-card>

            <!-- BERT Detection Result Card -->
            <v-card class="mb-6" elevation="2" rounded="lg">
              <v-card-title class="pa-6">
                <v-icon color="primary" class="mr-2">mdi-brain</v-icon>
                <span class="text-h6">BERT 检测结果</span>
              </v-card-title>
              <v-card-text class="pa-6 pt-0">
                <v-row>
                  <v-col cols="12" md="6">
                    <div class="text-subtitle-2 font-weight-bold mb-2">AI生成概率</div>
                    <v-progress-linear
                      :model-value="getAigcProbability(selectedReviewSection) * 100"
                      :color="getProbabilityColor(getAigcProbability(selectedReviewSection))"
                      height="28"
                      rounded
                    >
                      <template #default="{ value }">
                        <strong>{{ value.toFixed(1) }}%</strong>
                      </template>
                    </v-progress-linear>
                  </v-col>
                  <v-col cols="12" md="6">
                    <div class="text-subtitle-2 font-weight-bold mb-2">概率分布</div>
                    <div class="d-flex align-center gap-4">
                      <div class="flex-grow-1">
                        <div class="text-caption text-grey mb-1">人类撰写</div>
                        <v-progress-linear
                          :model-value="(selectedReviewSection.probabilities?.human || 0) * 100"
                          color="success"
                          height="12"
                          rounded
                        />
                        <div class="text-caption text-right">{{ ((selectedReviewSection.probabilities?.human || 0) * 100).toFixed(1) }}%</div>
                      </div>
                      <div class="flex-grow-1">
                        <div class="text-caption text-grey mb-1">AI生成</div>
                        <v-progress-linear
                          :model-value="(selectedReviewSection.probabilities?.aigc || 0) * 100"
                          color="error"
                          height="12"
                          rounded
                        />
                        <div class="text-caption text-right">{{ ((selectedReviewSection.probabilities?.aigc || 0) * 100).toFixed(1) }}%</div>
                      </div>
                    </div>
                  </v-col>
                </v-row>
                <div v-if="selectedReviewSection.label_name" class="mt-4">
                  <v-chip
                    :color="selectedReviewSection.is_aigc ? 'error' : 'success'"
                    variant="tonal"
                  >
                    模型判定：{{ getModelLabel(selectedReviewSection) }}，{{ getPredictionConfidenceLabel(selectedReviewSection) }} {{ formatProbability(getPredictionConfidence(selectedReviewSection)) }}
                  </v-chip>
                </div>
              </v-card-text>
            </v-card>

            <!-- Review Text Content Card -->
            <v-card class="mb-6" elevation="2" rounded="lg">
              <v-card-title class="pa-6">
                <v-icon color="info" class="mr-2">mdi-text-box</v-icon>
                <span class="text-h6">段落内容</span>
              </v-card-title>
              <v-card-text class="pa-6 pt-0">
                <div v-if="selectedReviewSection.text" class="paragraph-detail-text">{{ selectedReviewSection.text }}</div>
                <div v-else class="text-center py-8">
                  <v-icon size="48" color="grey-lighten-1">mdi-text-box-remove-outline</v-icon>
                  <div class="text-body-1 text-grey mt-2">该段落文本内容未保存</div>
                  <div class="text-caption text-grey mt-1">请重新执行检测以获取完整文本数据</div>
                </div>
              </v-card-text>
            </v-card>

          </template>
        </v-col>
      </v-row>
    </template>

    <!-- ========== Section Detail Dialog (for TOP5 clicks) ========== -->
    <v-dialog v-model="showParagraphDialog" max-width="800">
      <v-card v-if="selectedParagraph" rounded="lg">
        <v-card-title class="pa-6 d-flex align-center">
          <v-icon :color="getProbabilityColor(getAigcProbability(selectedParagraph))" class="mr-2">
            {{ getAigcProbability(selectedParagraph) > 0.5 ? 'mdi-alert-circle' : 'mdi-information' }}
          </v-icon>
          <span class="text-h6">{{ selectedParagraph.title || selectedParagraph.item_id }} 详情</span>
          <v-spacer />
          <v-btn icon="mdi-close" variant="text" @click="showParagraphDialog = false" />
        </v-card-title>

        <v-card-text class="pa-6">
          <!-- AI probability chips -->
          <div class="mb-4">
            <v-chip :color="getProbabilityColor(getAigcProbability(selectedParagraph))" size="large">
              <v-icon start>mdi-brain</v-icon>
              AI生成概率: {{ formatProbability(getAigcProbability(selectedParagraph)) }}
            </v-chip>
            <v-chip
              :color="getProbabilityColor(getAigcProbability(selectedParagraph))"
              size="large"
              class="ml-2"
            >
              {{ getProbabilityLevel(getAigcProbability(selectedParagraph)) }}
            </v-chip>
            <v-chip v-if="selectedParagraph.source_file" size="large" class="ml-2" variant="tonal">
              {{ selectedParagraph.source_file }}
            </v-chip>
          </div>

          <!-- Paragraph text -->
          <div class="mb-4">
            <h3 class="text-h6 mb-2">段落内容</h3>
            <div class="paragraph-detail-text">{{ selectedParagraph.text || '该段落文本内容未保存' }}</div>
          </div>

          <!-- Probability visual -->
          <div class="mb-4">
            <h3 class="text-h6 mb-2">AI生成概率可视化</h3>
            <v-progress-linear
              :model-value="getAigcProbability(selectedParagraph) * 100"
              :color="getProbabilityColor(getAigcProbability(selectedParagraph))"
              height="30"
            >
              <template #default="{ value }">
                <strong>{{ value.toFixed(1) }}%</strong>
              </template>
            </v-progress-linear>
          </div>

          <!-- Probability breakdown -->
          <div>
            <h3 class="text-h6 mb-2">概率分布</h3>
            <v-row>
              <v-col cols="6">
                <div class="text-body-2 mb-1">人类撰写</div>
                <v-progress-linear
                  :model-value="(selectedParagraph.probabilities?.human || 0) * 100"
                  color="success"
                  height="20"
                  rounded
                >
                  <template #default="{ value }">
                    <strong>{{ value.toFixed(1) }}%</strong>
                  </template>
                </v-progress-linear>
              </v-col>
              <v-col cols="6">
                <div class="text-body-2 mb-1">AI生成</div>
                <v-progress-linear
                  :model-value="(selectedParagraph.probabilities?.aigc || 0) * 100"
                  color="error"
                  height="20"
                  rounded
                >
                  <template #default="{ value }">
                    <strong>{{ value.toFixed(1) }}%</strong>
                  </template>
                </v-progress-linear>
              </v-col>
            </v-row>
          </div>
        </v-card-text>

        <v-card-actions class="pa-6 pt-0">
          <v-spacer />
          <v-btn color="primary" @click="showParagraphDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ========== Review Submission Card (Inline) ========== -->
    <v-row class="mt-6">
      <v-col cols="12">
        <v-card elevation="2" rounded="lg" class="pa-6">
          <v-card-title class="pa-0 mb-4 d-flex align-center">
            <v-icon color="success" class="mr-2">mdi-account-check</v-icon>
            <span class="text-h6">提交人工审核</span>
            <v-spacer />
            <v-chip size="small" :color="selectedSectionIds.size > 0 ? 'primary' : 'default'" variant="tonal">
              已选择 {{ selectedSectionIds.size }} 个段落
            </v-chip>
          </v-card-title>

          <v-card-text class="pa-0">
            <v-row>
              <!-- Left: Selected sections summary -->
              <v-col cols="12" md="6">
                <div class="text-subtitle-2 font-weight-bold mb-3">
                  <v-icon size="small" class="mr-1">mdi-file-document-multiple</v-icon>
                  已选择段落
                </div>
                <div v-if="selectedSectionIds.size === 0" class="text-body-2 text-grey pa-4 text-center rounded-lg border">
                  请在上方段落列表中勾选需要审核的段落
                </div>
                <div v-else class="selected-sections-preview">
                  <v-chip
                    v-for="id in [...selectedSectionIds].slice(0, 10)"
                    :key="id"
                    size="small"
                    closable
                    class="ma-1"
                    @click:close="toggleSectionSelection(id)"
                  >
                    {{ structuredSections.find(s => s.item_id === id)?.title || structuredReviewSections.find(s => s.item_id === id)?.title || id }}
                  </v-chip>
                  <div v-if="selectedSectionIds.size > 10" class="text-caption text-grey mt-1">
                    ...及其他 {{ selectedSectionIds.size - 10 }} 个段落
                  </div>
                </div>
              </v-col>

              <!-- Right: Reviewer selection + submit -->
              <v-col cols="12" md="6">
                <div class="text-subtitle-2 font-weight-bold mb-3">
                  <v-icon size="small" class="mr-1">mdi-account-group</v-icon>
                  选择审核人员
                </div>
                <v-autocomplete
                  v-model="selectedReviewers"
                  :items="allReviewers"
                  v-model:search="reviewSearchQuery"
                  item-title="username"
                  item-value="id"
                  label="搜索并选择审核人员"
                  multiple
                  chips
                  closable-chips
                  hide-details
                  variant="outlined"
                  class="mb-3"
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

                <!-- Reason textarea -->
                <v-textarea
                  v-model="reviewReason"
                  label="审核原因（选填）"
                  variant="outlined"
                  rows="2"
                  hide-details
                  class="mb-4"
                />

                <!-- Submit button -->
                <div class="d-flex justify-end gap-3">
                  <v-btn
                    :color="isDarkMode ? 'green-darken-2' : 'success'"
                    variant="outlined"
                    prepend-icon="mdi-select-all"
                    :disabled="textList.length === 0"
                    @click="selectAllSections('paper'); selectAllSections('review')"
                  >
                    全选段落
                  </v-btn>
                  <v-btn
                    variant="outlined"
                    @click="clearReviewSelection"
                    :disabled="selectedSectionIds.size === 0 && selectedReviewers.length === 0"
                  >
                    清空选择
                  </v-btn>
                  <v-btn
                    color="success"
                    variant="elevated"
                    prepend-icon="mdi-send"
                    :disabled="!canSubmitReview"
                    :loading="submittingReview"
                    @click="submitReview"
                  >
                    提交审核
                  </v-btn>
                </div>
              </v-col>
            </v-row>
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
            <pre class="raw-json-pre">{{ JSON.stringify(taskMeta, null, 2) }}</pre>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
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

.analysis-panel {
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
  border: 1px solid #dbeafe;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.86);
}

.analysis-panel .text-grey {
  color: #64748b !important;
}

.risk-distribution-row {
  padding: 12px;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.risk-distribution-row:not(:last-child) {
  margin-bottom: 12px;
}

.dimension-card {
  min-height: 176px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.dimension-card:hover {
  border-color: rgba(var(--v-theme-primary), 0.35);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
}

.dimension-score-row {
  display: flex;
  align-items: baseline;
  min-height: 32px;
}

.dimension-score {
  font-size: 1.45rem;
  font-weight: 700;
  line-height: 1.2;
}

/* Section list styles */
.section-list-container {
  max-height: 600px;
  overflow-y: auto;
}

.section-list-item {
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.section-list-item:hover {
  background-color: #f5f5f5;
  transform: translateX(4px);
}

.section-selected {
  border-color: rgb(var(--v-theme-primary));
  background-color: rgba(var(--v-theme-primary), 0.05);
  box-shadow: 0 2px 8px rgba(var(--v-theme-primary), 0.15);
}

.section-checked {
  border-color: rgb(var(--v-theme-primary));
  background-color: rgba(var(--v-theme-primary), 0.03);
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

.gap-3 {
  gap: 12px;
}

.gap-4 {
  gap: 16px;
}

.cursor-pointer {
  cursor: pointer;
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

<template>
  <div class="task-detail pa-4">
    <!-- 杩斿洖鎸夐挳 -->
    <div class="d-flex align-center mb-6">
      <v-btn icon="mdi-arrow-left" variant="text" @click="router.back()" class="mr-2 return-btn">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <span class="text-h6 font-weight-medium">杩斿洖鎴戠殑浠诲姟</span>
    </div>

    <!-- 涓昏鍐呭鍖哄煙 -->
    <div class="main-content rounded-lg">
      <!-- 椤堕儴淇℃伅鍖哄煙 -->
      <div class="info-section pa-6">
        <div class="content-wrapper d-flex justify-center">
          <div class="content-container">
            <div class="info-content d-flex align-center justify-space-between pa-4">
              <!-- 宸︿晶杩涘害鍜屾爣绛?-->
              <div class="d-flex align-center" style="min-width: 320px; margin-left: 200px">
                <div class="progress-circle mr-3 elevation-1">
                  <span class="text-h5 font-weight-bold primary--text">{{
                    formatNumber(overallScore) }}</span>
                  <span class="text-caption">涓哄亣</span>
                </div>
                <v-btn-toggle v-if="hasImages && hasTexts" v-model="reviewMode" mandatory class="ml-4">
                  <v-btn value="image" size="small">鍥剧墖</v-btn>
                  <v-btn value="text" size="small">鏂囨湰</v-btn>
                </v-btn-toggle>
                <v-card class="ml-4 pa-2 elevation-1" flat rounded="lg" width="250">
                  <v-card-title class="pa-2 pb-1 text-subtitle-2 font-weight-bold">AI 检测结果</v-card-title>
                  <v-card-text class="pa-2 pt-1">
                    <template v-if="!isTextMode">
                      <div v-for="(dimension, index) in detection_results" :key="index"
                        class="d-flex justify-space-between text-body-2 text-grey">
                        <span class="font-weight-medium">{{ convert(index) }}:</span>
                        <span class="text-primary">{{ dimension.probability.toFixed(2) }}</span>
                      </div>
                    </template>
                    <template v-else>
                      <div class="text-body-2 text-grey">文本人工审核不展示图片维度。</div>
                    </template>
                  </v-card-text>
                </v-card>
              </div>

              <!-- 鍙充晶浠诲姟淇℃伅 -->
              <div class="task-stats d-flex align-center">
                <div class="answer-card">

                  <v-row align="center" justify="start">
                    <v-col class="d-flex" cols="auto">
                      <div class="text-h6 font-weight-medium mb-4">瀹℃牳杩涘害</div>
                    </v-col>
                    <v-col class="d-flex align-center ml-4" cols="auto">
                      <v-btn color="primary" @click="handleSubmit">
                        鎻愪氦
                      </v-btn>
                    </v-col>
                  </v-row>
                  <div class="answer-grid">
                    <v-btn v-for="(_, index) in reviewItems" :key="index" :color="getAnswerButtonColor(index)"
                      variant="outlined" size="small" class="answer-btn" density="compact"
                      @click="handleResourceSelect(index)">
                      {{ index + 1 }}
                    </v-btn>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 鍒嗗壊绾?-->
      <v-divider></v-divider>

      <!-- 涓昏鍐呭鍖哄煙 -->
      <div class="content-wrapper d-flex pa-2 justify-center">
        <div class="content-container d-flex" style="gap: 12px;">
          <div v-if="!isTextMode" class="image-list rounded-lg elevation-1"
            style="background-color: rgb(var(--v-theme-surface)); padding: 20px;">
            <div class="text-h6 font-weight-medium text-center mb-4" style="white-space: nowrap;">鍥剧墖鍒楄〃</div>
            <div class="image-grid">
              <div v-for="(image, index) in images" :key="index" class="image-grid-item"
                :class="{ 'active': currentImageIndex === index }" @click="handleImageSelect(index)">
                <v-img :src="getImageUrl(image.url)" cover width="100%" height="100%" class="rounded-lg"></v-img>
              </div>
            </div>
          </div>
          <div v-else class="image-list rounded-lg elevation-1"
            style="background-color: rgb(var(--v-theme-surface)); padding: 20px;">
            <div class="text-h6 font-weight-medium text-center mb-4" style="white-space: nowrap;">鏂囨湰鍒楄〃</div>
            <div class="image-grid">
              <div v-for="(text, index) in texts" :key="index" class="image-grid-item"
                :class="{ 'active': currentTextIndex === index }" @click="handleTextSelect(index)">
                <div class="d-flex align-center justify-center h-100 text-caption">鏂囨湰 {{ index + 1 }}</div>
              </div>
            </div>
          </div>

          <div class="preview-section">
            <div class="preview-box">
              <template v-if="!isTextMode">
                <v-img v-if="currentImage" :src="getImageUrl(currentImage.url)" contain height="100%"
                  class="rounded-lg"></v-img>
                <template v-for="(dimension, index) in dimensionsPerImage[currentImageIndex]" :key="index">
                  <canvas v-show="currentDrawingDimension === index"
                    :ref="el => { if (el) drawingCanvases[index] = el as HTMLCanvasElement }" class="drawing-canvas"
                    :class="{ 'active': currentDrawingDimension === index }"
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"></canvas>
                </template>
                <transition name="fade">
                  <v-img v-if="activeOverlay && isOverlayVisible" :src="activeOverlay"
                    class="rounded-lg overlay-image"></v-img>
                </transition>
                <div class="preview-controls">
                  <v-btn icon="mdi-chevron-left" variant="flat" @click="handlePrevImage"
                    :disabled="currentImageIndex <= 0" class="control-btn" color="black" size="x-large"></v-btn>
                  <v-btn icon="mdi-chevron-right" variant="flat" @click="handleNextImage"
                    :disabled="currentImageIndex >= images.length - 1" class="control-btn" color="black"
                    size="x-large"></v-btn>
                </div>
              </template>
              <template v-else>
                <template v-if="currentText">
                  <div v-if="currentPreviewUrl" class="w-100 h-100">
                    <iframe :src="currentPreviewUrl" class="w-100 h-100" frameborder="0"></iframe>
                  </div>
                  <v-card v-else flat class="w-100 h-100 overflow-y-auto" color="transparent">
                    <v-card-text class="text-body-2" style="white-space: pre-wrap;">
                      {{ currentText.raw_text }}
                    </v-card-text>
                  </v-card>
                </template>
                <div v-else class="text-h6 text-grey">鏆傛棤鏂囨湰</div>
                <div class="preview-controls">
                  <v-btn icon="mdi-chevron-left" variant="flat" @click="handlePrevText"
                    :disabled="currentTextIndex <= 0" class="control-btn" color="black" size="x-large"></v-btn>
                  <v-btn icon="mdi-chevron-right" variant="flat" @click="handleNextText"
                    :disabled="currentTextIndex >= texts.length - 1" class="control-btn" color="black"
                    size="x-large"></v-btn>
                </div>
              </template>
            </div>
          </div>

          <div v-if="!isTextMode" class="dimension-section rounded-lg elevation-1">
            <div class="text-h6 font-weight-medium mb-4">璇勫垎缁村害</div>
            <div class="text-caption text-medium-emphasis mb-4">
              请根据图片特征，对每一种造假方式进行可能性评估，必要时可使用绘制标注功能标记具体位置。</div>
            <div class="dimension-list">
              <div v-for="(dimension, index) in dimensionsPerImage[currentImageIndex]" :key="index"
                class="dimension-item mb-6">
                <div class="d-flex align-center justify-space-between mb-2">
                  <span class="text-subtitle-1">{{ dimension.name }}</span>
                  <div class="d-flex">
                    <v-btn size="small" color="primary" variant="tonal" @click="openDrawingDialog(index)" class="mr-2">
                      <v-icon size="small" icon="mdi-pencil" class="mr-1"></v-icon>
                      缁樺埗鏍囨敞
                    </v-btn>
                    <v-btn size="small" :color="urn[index]?.visible ? 'error' : 'grey'" variant="tonal"
                      @click="handleDisplayFake(urn[index])" class="fake-area-btn">
                      <v-icon size="small" :icon="urn[index]?.visible ? 'mdi-eye-off' : 'mdi-eye'"
                        class="mr-1"></v-icon>
                      {{ urn[index]?.visible ? '闅愯棌閫犲亣鍖哄煙' : '鏄剧ず閫犲亣鍖哄煙' }}
                    </v-btn>
                  </div>
                </div>
                <div class="degree-buttons mb-2">
                  <v-btn-group variant="outlined" class="d-flex">
                    <v-btn v-for="option in degreeOptions" :key="option.value"
                      :color="dimension.value === option.value ? getDegreeColor(option.value) : 'grey'"
                      :variant="dimension.value === option.value ? 'flat' : 'outlined'" class="flex-grow-1"
                      @click="dimension.value = option.value" size="small">
                      {{ option.value }}
                    </v-btn>
                  </v-btn-group>
                </div>
                <v-text-field v-model="dimension.reason" :label="`请输入${dimension.name}的理由`" variant="outlined"
                  density="compact" hide-details class="mt-2"></v-text-field>
              </div>

              <div class="fake-judge-section mt-4 pt-4">
                <div class="text-subtitle-1 mb-4">閫犲亣鍒ゅ畾</div>
                <div class="d-flex justify-space-between">
                  <v-btn :color="imageJudgements[currentImageIndex] === true ? 'error' : 'grey-lighten-1'"
                    variant="tonal" class="flex-grow-1 mr-2" @click="handleJudgement(true)">
                    閫犲亣鍥剧墖
                  </v-btn>
                  <v-btn :color="imageJudgements[currentImageIndex] === false ? 'success' : 'grey-lighten-1'"
                    variant="tonal" class="flex-grow-1" @click="handleJudgement(false)">
                    鐪熷疄鍥剧墖
                  </v-btn>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="dimension-section rounded-lg elevation-1">
            <div class="text-h6 font-weight-medium mb-4">鏂囨湰瀹℃牳</div>
            <div class="text-caption text-medium-emphasis mb-4">请对当前文本给出人工审核结论与说明。</div>
            <v-textarea v-model="textComments[currentTextIndex]" label="瀹℃牳璇存槑" variant="outlined" rows="6"
              hide-details class="mb-4"></v-textarea>
            <v-text-field v-if="isReviewText" v-model.number="textTemplateScores[currentTextIndex]" type="number"
              label="妯℃澘鍖栧€惧悜澶嶆牳璇勫垎(0-1)" min="0" max="1" step="0.01" variant="outlined" hide-details
              class="mb-4"></v-text-field>
            <v-textarea v-if="isReviewText" v-model="textTemplateComments[currentTextIndex]" label="妯℃澘鍖栧€惧悜璇存槑"
              variant="outlined" rows="3" hide-details class="mb-4"></v-textarea>
            <div class="fake-judge-section mt-2 pt-2">
              <div class="text-subtitle-1 mb-4">鎬讳綋鍒ゅ畾</div>
              <div class="d-flex justify-space-between">
                <v-btn :color="textJudgements[currentTextIndex] === true ? 'error' : 'grey-lighten-1'"
                  variant="tonal" class="flex-grow-1 mr-2" @click="handleTextJudgement(true)">
                  鐤戜技AI
                </v-btn>
                <v-btn :color="textJudgements[currentTextIndex] === false ? 'success' : 'grey-lighten-1'"
                  variant="tonal" class="flex-grow-1" @click="handleTextJudgement(false)">
                  浜哄伐鎾板啓
                </v-btn>
              </div>
            </div>
            <div v-if="currentTextItems.length" class="mb-4">
              <div class="text-subtitle-2 mb-2">缁嗗垎娈佃惤瀹℃牳</div>
              <v-card v-for="(item, idx) in currentTextItems" :key="item.item_id || idx" variant="outlined" class="mb-3">
                <v-card-text>
                  <div class="d-flex align-center justify-space-between mb-2">
                    <div class="text-caption">
                      <span v-if="item.paragraph_index">娈佃惤 {{ item.paragraph_index }}</span>
                      <span v-else>鏉＄洰 {{ idx + 1 }}</span>
                      <span v-if="item.item_id">({{ item.item_id }})</span>
                    </div>
                    <v-chip v-if="item.ai_probability !== undefined && item.ai_probability !== null" size="small" color="primary" variant="outlined">
                      AI姒傜巼 {{ (item.ai_probability * 100).toFixed(1) }}%
                    </v-chip>
                  </div>
                  <div class="text-body-2 mb-3" style="white-space: pre-wrap;">{{ item.text || '' }}</div>
                  <div class="d-flex justify-space-between mb-2">
                    <v-btn
                      :color="textItemReviews[currentTextIndex][idx].is_ai_agreed === true ? 'error' : 'grey-lighten-1'"
                      variant="tonal" class="flex-grow-1 mr-2" @click="handleTextItemJudgement(idx, true)">
                      鐤戜技AI
                    </v-btn>
                    <v-btn
                      :color="textItemReviews[currentTextIndex][idx].is_ai_agreed === false ? 'success' : 'grey-lighten-1'"
                      variant="tonal" class="flex-grow-1" @click="handleTextItemJudgement(idx, false)">
                      浜哄伐鎾板啓
                    </v-btn>
                  </div>
                  <v-textarea
                    v-model="textItemReviews[currentTextIndex][idx].comment"
                    label="娈佃惤瀹℃牳璇存槑"
                    variant="outlined"
                    rows="2"
                    hide-details
                  ></v-textarea>
                </v-card-text>
              </v-card>
            </div>
            <div v-else class="text-body-2 text-grey">鏆傛棤鐤戜技AI鏉＄洰</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 娣诲姞鎻愮ず瀵硅瘽妗?-->
    <v-dialog v-model="showAlert" max-width="400">
      <v-card>
        <v-card-text class="pa-4">
          <div class="text-center">{{ alertMessage }}</div>
        </v-card-text>
        <v-card-actions class="justify-center pb-4">
          <v-btn color="primary" variant="text" @click="showAlert = false">
            纭畾
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 缁樺埗寮圭獥 -->
    <DrawingDialog v-model="showDrawingDialog" :image-url="currentImage ? getImageUrl(currentImage.url) : ''"
      :initial-paths="currentDimensionPaths" @save="handleDrawingSave" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import reviewer from '@/api/reviewer'
import type { RouteParams } from 'vue-router'
import { useSnackbarStore } from '@/stores/snackbar'
import DrawingDialog from '@/components/DrawingDialog.vue'
import publisher from '@/api/publisher'
import { appendPreviewToken, resolveApiAssetUrl } from '@/utils/preview-url'

const router = useRouter()
const snackbar = useSnackbarStore()
const route = useRoute()

interface Image {
  id: number,
  url: string
}

interface TextResource {
  id: number
  raw_text: string
  source_type?: string
  items?: TextEvidenceItem[]
  source_file_id?: number | null
}

interface TextEvidenceItem {
  item_id?: string
  paragraph_index?: number
  text?: string
  ai_probability?: number
  human_probability?: number
  is_aigc?: boolean
  label_name?: string
  confidence_score?: number
  reason?: string
}

interface TextItemReview {
  item_id?: string
  paragraph_index?: number
  text?: string
  is_ai_agreed: boolean | null
  comment: string
}

interface SubMethod {
  method: string
  probability: number
  mask_image: string
  mask_matrix: any | null
  visible: boolean
}

// 鍥剧墖鐩稿叧鏁版嵁鍜屾柟娉?
const currentImageIndex = ref(0)
const images = ref<Image[]>([])
const texts = ref<TextResource[]>([])
const taskType = ref('image')
const reviewMode = ref<'image' | 'text'>('image')

const manual_review_id = computed(() => (route.params as RouteParams & { manual_review_id: number }).manual_review_id)
const imageJudgements = ref<(boolean | null)[]>([])
const dimensionsPerImage = ref<Dimension[][]>([])
const urn = ref<SubMethod[]>([])
const activeOverlay = ref()
const isOverlayVisible = ref(false)
const overall = ref()
const detection_results = ref<dimension[]>([])
const currentTextIndex = ref(0)
const textJudgements = ref<(boolean | null)[]>([])
const textComments = ref<string[]>([])
const textTemplateScores = ref<(number | null)[]>([])
const textTemplateComments = ref<string[]>([])
const textItemReviews = ref<TextItemReview[][]>([])

const hasImages = computed(() => images.value.length > 0)
const hasTexts = computed(() => texts.value.length > 0)
const isTextMode = computed(() => reviewMode.value === 'text')
const isReviewText = computed(() => taskType.value === 'review_text')
const reviewItems = computed(() => (isTextMode.value ? texts.value : images.value))
const overallScore = computed(() => overall.value?.confidence_score ?? 0)

interface dimension {
  method: string,
  probability: number
}

const convert = (index: number) => {
  switch (index) {
    case 0:
      return '高斯模糊'
    case 1:
      return '亮度/对比度调节'
    case 2:
      return '智能修复'
    case 3:
      return '暴力覆盖'
    case 4:
      return '同图复制'
    case 5:
      return '重录切割'
    case 6:
      return '跨图拼接'
  }
}


const fetchDetectionResults = async () => {
  try {
    if (!currentImage.value) {
      return
    }
    const id = await (await publisher.getDetectionID({ img_id: currentImage.value?.id })).data.detection_result_id
    const response = (await publisher.getSingleImageResult(id)).data
    detection_results.value = response.sub_methods
  } catch (error) {
    snackbar.showMessage('获取检测结果失败', 'error')
  }
}


const formatNumber = (result: number) => {
  const value = Number(result)
  if (!Number.isFinite(value)) {
    return '0.00%'
  }
  return `${(value * 100).toFixed(2)}%`
}


onMounted(async () => {
  try {
    const response = (await reviewer.getReviewTaskDetail({ manual_review_id: manual_review_id.value })).data
    images.value = Array.isArray(response.imgs) ? response.imgs : []
    texts.value = (Array.isArray(response.texts) ? response.texts : []).map(text => ({
      ...text,
      items: Array.isArray(text.items) ? text.items.filter(item => item.is_aigc === true) : []
    }))
    taskType.value = response.task_type || (texts.value.length ? 'paper_text' : 'image')
    reviewMode.value = texts.value.length && !images.value.length ? 'text' : 'image'
    overall.value = response.ai_detection_result || null
    imageJudgements.value = new Array(images.value.length).fill(null)
    textJudgements.value = new Array(texts.value.length).fill(null)
    textComments.value = new Array(texts.value.length).fill('')
    textTemplateScores.value = new Array(texts.value.length).fill(null)
    textTemplateComments.value = new Array(texts.value.length).fill('')
    textItemReviews.value = texts.value.map(text => {
      const items = Array.isArray(text.items) ? text.items : []
      return items.map(item => ({
        item_id: item.item_id,
        paragraph_index: item.paragraph_index,
        text: item.text,
        is_ai_agreed: null,
        comment: ''
      }))
    })

    // 涓烘瘡涓浘鐗囩殑姣忎釜缁村害鍒濆鍖栫嫭绔嬬殑鏁版嵁
    dimensionsPerImage.value = images.value.map(() => [
      { name: '高斯模糊', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
      { name: '亮度/对比度调节', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
      { name: '智能修复', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
      { name: '暴力覆盖', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
      { name: '同图复制', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
      { name: '重录切割', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
      { name: '跨图拼接', value: null, reason: '', showFakeArea: false, drawingPaths: [] }
    ])
    if (images.value.length) {
      fetchMaskImage()
      fetchDetectionResults()
    }

  } catch (error) {
    snackbar.showMessage('鑾峰彇浠诲姟璇︽儏澶辫触', 'error')
  }
})

const currentImage = computed(() => {
  if (
    Array.isArray(images.value) &&
    typeof currentImageIndex.value === 'number' &&
    currentImageIndex.value >= 0 &&
    currentImageIndex.value < images.value.length
  ) {
    return images.value[currentImageIndex.value];
  }
  return null;
});

const currentText = computed(() => {
  if (
    Array.isArray(texts.value) &&
    typeof currentTextIndex.value === 'number' &&
    currentTextIndex.value >= 0 &&
    currentTextIndex.value < texts.value.length
  ) {
    return texts.value[currentTextIndex.value]
  }
  return null
})

const currentTextItems = computed(() => {
  const current = texts.value[currentTextIndex.value]
  return Array.isArray(current?.items) ? current.items : []
})

const currentPreviewUrl = computed(() => {
  const fileId = currentText.value?.source_file_id
  if (!fileId) {
    return ''
  }
  return appendPreviewToken(resolveApiAssetUrl(`/api/preview/file/${fileId}/`))
})

const getImageUrl = (url: string) => {
  return import.meta.env.VITE_API_URL + url
}

const fetchMaskImage = async () => {
  try {
    if (!currentImage.value) {
      return
    }
    const res = (await reviewer.getMaskImage({ img_id: currentImage.value?.id })).data
    urn.value = res.sub_methods.map((item: Omit<SubMethod, 'visible'>) => ({
      ...item,
      visible: false
    }))
    overall.value = res.overall
  } catch (error) {
    snackbar.showMessage('鑾峰彇mask澶辫触', 'error')
  }
}

const handleDisplayFake = (dimension: SubMethod) => {
  if (dimension.visible) {
    dimension.visible = false
    isOverlayVisible.value = false
    activeOverlay.value = null
    return
  }

  // 鍏抽棴鍏朵粬鎵€鏈夎鐩栧眰
  urn.value.forEach(d => {
    if (d !== dimension) {
      d.visible = false
    }
  })

  // 鏄剧ず褰撳墠瑕嗙洊灞?
  dimension.visible = true
  isOverlayVisible.value = true
  activeOverlay.value = dimension.mask_image
}

const handleImageSelect = (index: number) => {
  currentImageIndex.value = index
  currentDrawingDimension.value = -1 // 閲嶇疆缁樺埗鐘舵€?
  fetchMaskImage()
  fetchDetectionResults()
}

const handleTextSelect = (index: number) => {
  currentTextIndex.value = index
}

const handleTextItemJudgement = (index: number, value: boolean) => {
  const reviews = textItemReviews.value[currentTextIndex.value]
  if (!reviews || !reviews[index]) {
    return
  }
  reviews[index].is_ai_agreed = value
}

const handleResourceSelect = (index: number) => {
  if (isTextMode.value) {
    handleTextSelect(index)
  } else {
    handleImageSelect(index)
  }
}

const handlePrevImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
  }
}

const handleNextImage = () => {
  if (currentImageIndex.value < images.value.length - 1) {
    currentImageIndex.value++
  }
}

const handlePrevText = () => {
  if (currentTextIndex.value > 0) {
    currentTextIndex.value--
  }
}

const handleNextText = () => {
  if (currentTextIndex.value < texts.value.length - 1) {
    currentTextIndex.value++
  }
}

// 璇勫垎缁村害鏁版嵁
interface Dimension {
  name: string;
  value: number | null;
  reason: string;
  showFakeArea: boolean;
  drawingPaths: Array<{
    points: Array<{ x: number, y: number }>;
    color: string;
  }>;
}

const drawingCanvases = ref<HTMLCanvasElement[]>([])
const imageRect = ref<DOMRect | null>(null)
const currentDrawingDimension = ref<number>(-1)

// 璁＄畻褰撳墠缁村害鐨勭瑪杩瑰垪琛?
const currentDimensionPaths = computed(() => {
  if (currentDrawingDimension.value === -1) return []
  const currentImage = dimensionsPerImage.value[currentImageIndex.value]
  if (!currentImage) return []
  const currentDim = currentImage[currentDrawingDimension.value]
  return currentDim?.drawingPaths || []
})

// 鎵撳紑缁樺埗瀵硅瘽妗?
const openDrawingDialog = (index: number) => {
  currentDrawingDimension.value = index
  showDrawingDialog.value = true
}

// 澶勭悊缁樺埗淇濆瓨
const handleDrawingSave = (paths: Array<{ points: Array<{ x: number; y: number }>; color: string }>) => {
  if (currentDrawingDimension.value === -1) return

  const currentImage = dimensionsPerImage.value[currentImageIndex.value]
  if (!currentImage) return

  // 鍙洿鏂板綋鍓嶇淮搴︾殑缁樺埗璺緞
  currentImage[currentDrawingDimension.value].drawingPaths = [...paths]
}

// 鐩戝惉鍥剧墖鍔犺浇瀹屾垚
watch(() => currentImage.value?.url, () => {
  const imgElement = document.querySelector('.preview-box .v-img img') as HTMLImageElement
  if (imgElement) {
    if (imgElement.complete) {
      imageRect.value = imgElement.getBoundingClientRect()
    } else {
      imgElement.onload = () => {
        imageRect.value = imgElement.getBoundingClientRect()
      }
    }
  }
})

// 鐩戝惉绐楀彛澶у皬鍙樺寲
onMounted(() => {
  window.addEventListener('resize', () => {
    const imgElement = document.querySelector('.preview-box .v-img img') as HTMLImageElement
    if (imgElement) {
      imageRect.value = imgElement.getBoundingClientRect()
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', () => { })
})

const degreeOptions = [
  { value: 1, label: '轻微' },
  { value: 2, label: '一般' },
  { value: 3, label: '中等' },
  { value: 4, label: '明显' },
  { value: 5, label: '严重' }
]

const getDegreeColor = (value: number) => {
  switch (value) {
    case 1:
      return 'success'
    case 2:
      return 'info'
    case 3:
      return 'yellow'
    case 4:
      return 'warning'
    case 5:
      return 'error'
    default:
      return 'grey'
  }
}

// 澶勭悊閫犲亣鍒ゅ畾
const handleJudgement = (isFake: boolean) => {
  imageJudgements.value[currentImageIndex.value] = isFake
}

const handleTextJudgement = (isFake: boolean) => {
  textJudgements.value[currentTextIndex.value] = isFake
}

// 鑾峰彇绛旈鍗℃寜閽鑹?
const getAnswerButtonColor = (index: number) => {
  if (!isTextMode.value && index === currentImageIndex.value) return 'primary'
  if (isTextMode.value && index === currentTextIndex.value) return 'primary'
  const judgement = isTextMode.value ? textJudgements.value[index] : imageJudgements.value[index]
  if (judgement === null) return 'grey'
  return judgement ? 'error' : 'success'
}

const showAlert = ref(false)
const alertMessage = ref('')

const checkAnswerCompletion = () => {
  // 妫€鏌ユ瘡寮犲浘鐗囨槸鍚﹂兘宸插畬鎴愯瘎鍒嗗拰鍒ゅ畾
  for (let i = 0; i < images.value.length; i++) {
    // 妫€鏌ラ€犲亣鍒ゅ畾鏄惁宸插畬鎴?
    if (imageJudgements.value[i] === null) {
      return {
        complete: false,
        message: `绗?${i + 1} 寮犲浘鐗囧皻鏈繘琛岄€犲亣鍒ゅ畾`
      }
    }
  }

  for (let i = 0; i < dimensionsPerImage.value.length; i++) {
    const dims = dimensionsPerImage.value[i]

    const hasUnratedDimension = dims.some(dim => dim.value === null)
    if (hasUnratedDimension) {
      return {
        complete: false,
        message: `绗?${i + 1} 寮犲浘鐗囩殑璇勫垎缁村害灏氭湭璇勫垎瀹屾暣`
      }
    }

    const hasEmptyReason = dims.some(dim => !dim.reason)
    if (hasEmptyReason) {
      return {
        complete: false,
        message: `绗?${i + 1} 寮犲浘鐗囩殑璇勫垎缁村害鐞嗙敱灏氭湭濉啓瀹屾暣`
      }
    }
  }

  return {
    complete: true,
    message: '鎵€鏈夊浘鐗囧凡瀹屾垚璇勫垎'
  }
}

const checkTextCompletion = () => {
  for (let i = 0; i < texts.value.length; i++) {
    if (textJudgements.value[i] === null) {
      return {
        complete: false,
        message: `第 ${i + 1} 段文本尚未完成真假判定`
      }
    }
    if (!textComments.value[i]) {
      return {
        complete: false,
        message: `第 ${i + 1} 段文本尚未填写审核说明`
      }
    }

    const itemReviews = textItemReviews.value[i] || []
    const hasPendingItem = itemReviews.some(item => item.is_ai_agreed === null)
    if (hasPendingItem) {
      return {
        complete: false,
        message: `第 ${i + 1} 段文本的细分项尚未完成审核`
      }
    }
  }

  return {
    complete: true,
    message: '鎵€鏈夋枃鏈凡瀹屾垚瀹℃牳'
  }
}

interface ImageItem {
  img_id: number
  score: Array<number | null>  // 缁村害寰楀垎鏁扮粍锛屽彲鑳芥槸鏁板€兼垨鑰卬ull
  reason: Array<string | null>  // 缁村害鐞嗙敱鏁扮粍锛屽彲鑳芥槸瀛楃涓叉垨鑰卬ull
  final: boolean | null  // 閫犲亣鍒ゅ畾缁撴灉
  points: Array<Array<{}>>
}

interface TextItem {
  text_id: number
  overall_comment: string
  final: boolean | null
  paragraph_reviews?: TextItemReview[]
  template_review_score?: number | null
  template_review_comment?: string
}

const constructData = () => {
  const data: { result?: ImageItem[]; text_results?: TextItem[] } = {}

  if (images.value.length) {
    data.result = []
    for (let i = 0; i < images.value.length; i++) {
      const item: ImageItem = {
        img_id: images.value[i].id,
        score: dimensionsPerImage.value[i].map(dim => dim.value),
        reason: dimensionsPerImage.value[i].map(dim => dim.reason),
        final: imageJudgements.value[i],
        points: dimensionsPerImage.value[i].map(dim => dim.drawingPaths)
      }
      data.result.push(item)
    }
  }

  if (texts.value.length) {
    data.text_results = []
    for (let i = 0; i < texts.value.length; i++) {
      const paragraphReviews = (textItemReviews.value[i] || []).map(item => ({
        item_id: item.item_id,
        paragraph_index: item.paragraph_index,
        text: item.text,
        is_ai_agreed: item.is_ai_agreed,
        comment: item.comment
      }))
      const item: TextItem = {
        text_id: texts.value[i].id,
        overall_comment: textComments.value[i],
        final: textJudgements.value[i],
        paragraph_reviews: paragraphReviews,
        template_review_score: textTemplateScores.value[i] ?? null,
        template_review_comment: textTemplateComments.value[i]
      }
      data.text_results.push(item)
    }
  }

  return data
}

const handleSubmit = async () => {
  if (images.value.length) {
    const result = checkAnswerCompletion()
    if (!result.complete) {
      snackbar.showMessage(result.message, 'error')
      return
    }
  }

  if (texts.value.length) {
    const textCheck = checkTextCompletion()
    if (!textCheck.complete) {
      snackbar.showMessage(textCheck.message, 'error')
      return
    }
  }

  try {
    await reviewer.submitReview(manual_review_id.value, constructData())
    snackbar.showMessage('鎻愪氦鎴愬姛', 'success')
  } catch (error) {
    snackbar.showMessage('鎻愪氦澶辫触', 'error')
  }
}

const showDrawingDialog = ref(false)

// 鐩戝惉鍥剧墖鍒囨崲
watch(() => currentImageIndex.value, () => {
  currentDrawingDimension.value = -1 // 閲嶇疆缁樺埗鐘舵€?
})

// 鐩戝惉缁村害鍒囨崲
watch(() => currentDrawingDimension.value, (newVal, oldVal) => {
  // 纭繚鎵€鏈夌敾甯冮兘琚殣钘?
  drawingCanvases.value.forEach((canvas, index) => {
    if (canvas) {
      canvas.style.display = 'none'
    }
  })

  // 鍙樉绀哄綋鍓嶇淮搴︾殑鐢诲竷
  if (newVal !== -1) {
    const newCanvas = drawingCanvases.value[newVal]
    if (newCanvas) {
      newCanvas.style.display = 'block'
    }
  }
})
</script>

<style scoped>
.task-detail {
  position: relative;
  min-height: 100vh;
  max-height: 100vh;
  background-color: rgb(var(--v-theme-surface));
  overflow: hidden;
}

.main-content {
  height: calc(100vh - 80px);
  overflow: hidden;
  background-color: rgb(var(--v-theme-surface));
}

.info-section {
  background-color: rgb(var(--v-theme-surface));
  padding: 16px 0;
}

.info-content {
  width: 100%;
  background-color: rgb(var(--v-theme-surface));
  min-height: 160px;
  padding: 12px 16px !important;
  justify-content: center;
  gap: 24px;
}

.progress-circle {
  width: clamp(100px, 8vw, 130px);
  height: clamp(100px, 8vw, 130px);
  border-radius: 50%;
  border: 5px solid rgb(var(--v-theme-primary));
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgb(var(--v-theme-surface));
}

.progress-circle .text-h5 {
  font-size: clamp(1.8rem, 2vw, 2.5rem) !important;
  line-height: 1.2;
}

.progress-circle .text-caption {
  font-size: 1rem !important;
  margin-top: 4px;
}

.task-list {
  width: clamp(360px, 30vw, 420px);
  padding: 0 12px;
}

.task-item {
  width: 100%;
  margin-bottom: 12px;
}

.task-item .v-progress-linear {
  width: clamp(260px, 25vw, 340px) !important;
  height: 10px !important;
}

.task-item .text-h6 {
  white-space: nowrap;
}

.content-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.content-container {
  width: 100%;
  max-width: min(1200px, 95vw);
  display: flex;
  justify-content: center;
}

.task-stats {
  min-width: 320px;
  justify-content: center;
}

.answer-card {
  padding: 16px;
  border-radius: 8px;
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-width: 280px;
  margin-right: 200px
}

.answer-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.overlay-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  mix-blend-mode: multiply;
  opacity: 0.7;
  object-fit: contain;
}

.preview-box .control-btn {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}

.preview-box:hover .control-btn {
  opacity: 1;
  pointer-events: auto;
}

@media (hover: none) {
  .preview-box .control-btn {
    opacity: 1;
    pointer-events: auto;
  }
}


.answer-btn {
  width: 36px !important;
  min-width: 0 !important;
  height: 36px !important;
  padding: 0 !important;
}

@media (max-width: 1280px) {
  .task-stats {
    min-width: clamp(280px, 25vw, 320px);
  }

  .answer-card {
    padding: 12px;
  }

  .answer-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.image-list {
  width: clamp(100px, 8vw, 120px);
  height: calc(100vh - 380px);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.image-grid {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  margin-top: -8px;
}

.image-grid-item {
  width: 80px;
  height: 80px;
  cursor: pointer;
  border-radius: 4px;
  overflow: hidden;
  transition: border-color 0.2s ease;
  border: 2px solid transparent;
  flex-shrink: 0;
}

.image-grid-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.5);
}

.image-grid-item.active {
  border-color: rgb(var(--v-theme-primary));
}

.preview-section {
  flex: 1;
  min-width: 0;
  max-width: min(800px, 60vw);
  margin: 0 12px;
}

.preview-box {
  position: relative;
  height: calc(100vh - 380px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  overflow: hidden;
}

.preview-box .v-img {
  max-width: 800px;
  max-height: 100%;
  object-fit: contain;
}

.preview-controls {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 16px;
}

.control-btn {
  opacity: 0.7;
  transition: opacity 0.2s ease !important;
}

.control-btn:hover {
  opacity: 1;
  transform: none;
}

/* 婊氬姩鏉℃牱寮?*/
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.4);
}

@media (max-width: 960px) {
  .content-container {
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .preview-section {
    max-width: 100%;
    order: -1;
  }

  .image-list {
    height: auto;
    min-height: 300px;
  }

  .answer-card {
    padding: 12px;
  }

  .answer-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.dimension-section {
  width: 360px;
  padding: 20px;
  background-color: rgb(var(--v-theme-surface));
  height: calc(100vh - 380px);
  overflow-y: auto;
}

.dimension-list {
  padding-right: 12px;
}

.dimension-item {
  border-bottom: 1px solid rgba(var(--v-theme-primary), 0.1);
  padding-bottom: 16px;
}

.dimension-item:last-child {
  border-bottom: none;
}

@media (max-width: 1280px) {
  .dimension-section {
    width: 260px;
  }
}

.fake-judge-section {
  border-top: 1px solid rgba(var(--v-theme-primary), 0.1);
}

.degree-buttons {
  width: 100%;
}

.degree-buttons .v-btn {
  text-transform: none;
  letter-spacing: 0;
  font-size: 0.875rem;
}

.fake-area-btn {
  font-size: 0.75rem;
  text-transform: none;
  letter-spacing: 0;
  min-width: 120px;
  /* 纭繚鎸夐挳鏈夊浐瀹氱殑鏈€灏忓搴?*/
}

.drawing-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  display: none;
}

.drawing-canvas.active {
  pointer-events: auto;
  cursor: crosshair;
  display: block;
}

.color-preview {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}
</style>

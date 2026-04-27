<template>
  <v-row v-if="showMetaControls">
    <v-col cols="6" class="mb-2">
      <v-select v-model="selectedTag" :items="mappedTag" label="为本批图片添加标签" clearable variant="outlined" hide-details />
    </v-col>
    <v-col cols="6" class="mb-2">
      <v-text-field v-model="task_name" label="为该检测任务添加名称" @update:modelValue="handleName"
        variant="outlined" :rules="[v => !v || v.length <= 10 || '任务名称不能超过10个字']" counter="10"></v-text-field>
    </v-col>
  </v-row>


  <v-row>
    <v-col cols="12">
      <div class="d-flex align-center mb-4">
        <span class="text-h6">已提取图片</span>
      </div>
    </v-col>
  </v-row>

  <v-row>
    <!-- 左侧缩略图列表 -->
    <v-col cols="4" class="thumbnail-list pa-0" :class="{ 'full-height-panel': !compactMode }">
      <v-card :style="thumbnailCardStyle">
        <v-card-text class="pa-0" :style="thumbnailBodyStyle">
          <v-list lines="two" class="thumbnail-scroll" :style="thumbnailBodyStyle">
            <v-list-item v-for="(image, index) in pagedImages" :key="image.image_id"
              :class="{ 'selected-item': selectedImage?.image_id === image.image_id }" @click="selectImage(image)">
              <template v-slot:prepend>
                <v-avatar size="60" class="me-2">
                  <v-img :src="image.image_url" cover class="bg-grey-lighten-2"></v-img>
                </v-avatar>
              </template>
              <v-list-item-title>
                {{ `图片${(listPage - 1) * itemsPerPage + index + 1}` }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ image.extracted_from_pdf ? 'PDF提取' : '上传图片' }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <div class="d-flex justify-center py-3" v-if="pageCount > 1">
            <v-pagination v-model="listPage" :length="pageCount" :total-visible="5" density="comfortable"></v-pagination>
          </div>
        </v-card-text>
      </v-card>
    </v-col>

    <!-- 右侧大图预览 -->
    <v-col cols="8" class="preview-section pa-0" :class="{ 'full-height-panel': !compactMode }">
      <v-card :style="previewCardStyle">
        <v-card-text class="pa-0 preview-wrapper" :style="previewBodyStyle">
          <div v-if="selectedImage" class="preview-container" :style="previewBodyStyle">
            <v-btn icon="mdi-chevron-left" variant="text" size="x-large" class="preview-nav-btn preview-nav-left"
              :disabled="!canNavigatePrev" @click="navigatePrev"></v-btn>

            <div class="image-container">
              <v-img :src="selectedImage.image_url" class="preview-image" cover></v-img>
            </div>

            <v-btn icon="mdi-chevron-right" variant="text" size="x-large" class="preview-nav-btn preview-nav-right"
              :disabled="!canNavigateNext" @click="navigateNext"></v-btn>

            <div class="preview-info pa-4">
              <div class="text-h6">
                {{ `图片${currentIndex + 1}` }}
              </div>
              <div class="text-body-2">
                {{ selectedImage.extracted_from_pdf ? 'PDF提取' : '上传图片' }}
              </div>
            </div>
          </div>
          <div v-else class="d-flex align-center justify-center h-100">
            <div class="text-h6 text-grey">请选择一张图片查看详情</div>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useSnackbarStore } from '@/stores/snackbar';
import upload from '@/api/upload'

const snackbar = useSnackbarStore()
const task_name = ref('')

interface Image {
  image_id: number
  image_url: string
  page_number?: number
  extracted_from_pdf: boolean
}

const props = withDefaults(defineProps<{
  images?: Image[]
  fileId?: number
  fileIds?: number[]
  showMetaControls?: boolean
}>(), {
  images: () => [],
  fileId: 0,
  fileIds: () => [],
  showMetaControls: true
})

const showMetaControls = computed(() => props.showMetaControls)
// 多材料复用时隐藏顶部输入区，启用紧凑展示模式
const compactMode = computed(() => !showMetaControls.value)

const emit = defineEmits<{
  (e: 'tagChanged', tag: string): void
  (e: 'addName', task_name: string): void
}>()





// 使用响应式变量存储图片
const localImages = ref<Image[]>([])

// 使用计算属性合并props和本地图片
const displayImages = computed(() => {
  return localImages.value.length > 0 ? localImages.value : props.images
})

// 列表分页：每页最多展示5条
const itemsPerPage = 5
const listPage = ref(1)
const pageCount = computed(() => Math.max(1, Math.ceil(displayImages.value.length / itemsPerPage)))
const pagedImages = computed(() => {
  const start = (listPage.value - 1) * itemsPerPage
  return displayImages.value.slice(start, start + itemsPerPage)
})

// 紧凑模式下根据当前页条目数动态调整卡片高度
const visibleItemCount = computed(() => Math.max(1, Math.min(pagedImages.value.length, itemsPerPage)))
const thumbnailBodyStyle = computed(() => {
  if (!compactMode.value) {
    return {}
  }
  return {
    maxHeight: `${visibleItemCount.value * 84}px`,
    overflowY: 'auto' as const
  }
})

const thumbnailCardStyle = computed(() => {
  if (!compactMode.value) {
    return {}
  }
  return {
    minHeight: `${visibleItemCount.value * 84}px`
  }
})

const previewBodyStyle = computed(() => {
  if (!compactMode.value) {
    return {}
  }
  return {
    minHeight: selectedImage.value ? '320px' : `${visibleItemCount.value * 84}px`
  }
})

const previewCardStyle = computed(() => {
  if (!compactMode.value) {
    return {}
  }
  return {
    minHeight: selectedImage.value ? '320px' : `${visibleItemCount.value * 84}px`
  }
})

const loading = ref(false)
const pageSize = ref(50)
const loadedImageIds = ref<Set<number>>(new Set())

const resolveImageUrl = (path: string): string => {
  const apiBase = import.meta.env.VITE_API_URL || ''
  return apiBase ? `${apiBase}${path}` : path
}

const appendImages = (images: any[]) => {
  images.forEach(img => {
    const imageId = Number(img.image_id)
    if (!Number.isFinite(imageId) || loadedImageIds.value.has(imageId)) {
      return
    }
    loadedImageIds.value.add(imageId)
    localImages.value.push({
      image_id: imageId,
      image_url: resolveImageUrl(img.image_url),
      page_number: img.page_number,
      extracted_from_pdf: img.extracted_from_pdf
    })
  })
}

const loadImagesForFile = async (targetFileId: number) => {
  let pageNumber = 1
  let loadedCount = 0
  let total = 0

  do {
    const response = (await upload.getExtractedImages({
      file_id: targetFileId,
      page_number: pageNumber,
      page_size: pageSize.value
    })).data

    const fetchedImages = Array.isArray(response.images) ? response.images : []
    appendImages(fetchedImages)
    loadedCount += fetchedImages.length
    total = Number(response.total || 0)
    pageNumber += 1

    if (!fetchedImages.length) {
      break
    }
  } while (loadedCount < total)
}

const loadAllImages = async () => {
  const targets = props.fileIds.length
    ? props.fileIds
    : (props.fileId ? [props.fileId] : [])

  if (!targets.length) {
    return
  }

  loading.value = true
  try {
    localImages.value = []
    loadedImageIds.value = new Set<number>()
    for (const targetFileId of targets) {
      await loadImagesForFile(targetFileId)
    }
  } catch (error) {
    snackbar.showMessage('图片加载失败', 'error')
  } finally {
    loading.value = false
  }
}

const selectedImage = ref<Image | null>(null)
const currentIndex = ref(-1)

const selectImage = (image: Image) => {
  console.log(image)
  selectedImage.value = image
  currentIndex.value = displayImages.value.findIndex(img => img.image_id === image.image_id)
}


const canNavigatePrev = computed(() => currentIndex.value > 0)
const canNavigateNext = computed(() => currentIndex.value < displayImages.value.length - 1)

const navigatePrev = () => {
  if (canNavigatePrev.value) {
    currentIndex.value--
    selectedImage.value = displayImages.value[currentIndex.value]
  }
}

const navigateNext = () => {
  if (canNavigateNext.value) {
    currentIndex.value++
    selectedImage.value = displayImages.value[currentIndex.value]
  }
}

const handleName = () => {
  emit('addName', task_name.value)
}

// 获取提取的图片
onMounted(async () => {
  if (props.fileId || props.fileIds.length) {
    await loadAllImages()
  }
})

const mappedTag = [
  { title: '医学', value: 'Medicine' },
  { title: '生物', value: 'Biology' },
  { title: '化学', value: 'Chemistry' },
  { title: '图形学', value: 'Graphics' },
  { title: '其他', value: 'Other' }
]
const selectedTag = ref(null)


watch(selectedTag, (newVal) => {
  if (newVal !== null) {
    console.log('标签变为:', newVal)
    emit('tagChanged', newVal)
  } else {
    console.log('标签被清除')
  }
})

watch(displayImages, () => {
  // 列表总数变化时，自动修正越界页码
  if (listPage.value > pageCount.value) {
    listPage.value = pageCount.value
  }
}, { deep: true })

</script>

<style scoped>
.thumbnail-list {
  overflow: hidden;
}

.preview-section {
  overflow: hidden;
}

.full-height-panel {
  height: calc(100vh - 300px);
}

.thumbnail-scroll {
  overflow-y: auto;
  overflow-x: hidden;
}

.v-list {
  padding: 0;
}

.v-list-item {
  min-height: 80px;
  padding: 8px 16px;
}

.selected-item {
  background-color: rgb(var(--v-theme-primary), 0.1);
}

.preview-wrapper {
  position: relative;
  height: 100%;
}

.preview-container {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.image-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background-color: rgb(var(--v-theme-surface));
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
  width: auto;
  height: auto;
}

.preview-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
  background: rgba(0, 0, 0, 0.3) !important;
  color: white !important;
}

.preview-nav-btn:hover {
  background: rgba(0, 0, 0, 0.5) !important;
}

.preview-nav-left {
  left: 16px;
}

.preview-nav-right {
  right: 16px;
}

.preview-info {
  background: rgba(0, 0, 0, 0.5);
  color: white;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
}
</style>
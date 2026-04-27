<template>
  <v-row v-if="showMetaControls">
    <v-col cols="6" class="mb-2">
      <v-select
        v-model="selectedTag"
        :items="mappedTag"
        :label="`为本批${moduleLabel}内容添加标签`"
        clearable
        variant="outlined"
        hide-details
      />
    </v-col>
    <v-col cols="6" class="mb-2">
      <v-text-field
        v-model="taskName"
        label="为该检测任务添加名称"
        variant="outlined"
        :rules="[v => !v || v.length <= 10 || '任务名称不能超过10个字']"
        counter="10"
        @update:model-value="emitTaskName"
      />
    </v-col>
  </v-row>

  <v-row>
    <v-col cols="12">
      <div class="d-flex align-center mb-4">
        <span class="text-h6">已提取{{ moduleLabel }}内容</span>
      </div>
    </v-col>
  </v-row>

  <v-row>
    <v-col cols="4" class="content-list pa-0" :class="{ 'full-height-panel': !compactMode }">
      <v-card :style="listCardStyle">
        <v-card-text class="pa-0" :style="listBodyStyle">
          <v-list lines="two" class="content-scroll" :style="contentScrollStyle">
            <v-list-item
              v-if="previewMode === 'file'"
              v-for="file in previewFiles"
              :key="`preview-${file.file_id}`"
              :class="{ 'selected-item': activePreviewFileId === file.file_id }"
              @click="selectPreviewFile(file)"
            >
              <template #prepend>
                <v-avatar size="42" class="me-2" color="primary" variant="tonal">
                  <v-icon>mdi-file-eye-outline</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>{{ file.file_name || `${moduleLabel}原文件` }}</v-list-item-title>
              <v-list-item-subtitle>
                直接预览{{ file.file_ext ? `（${file.file_ext.toUpperCase()}）` : '' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item
              v-if="previewMode !== 'file'"
              v-for="(item, index) in pagedContents"
              :key="item.content_id"
              :class="{ 'selected-item': activeItem?.content_id === item.content_id }"
              @click="selectItem(item)"
            >
              <template #prepend>
                <v-avatar size="42" class="me-2" color="primary" variant="tonal">
                  <v-icon>{{ moduleIcon }}</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>{{ item.title || `${moduleLabel}片段${index + 1}` }}</v-list-item-title>
              <v-list-item-subtitle>{{ item.source || '提取内容' }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="previewMode !== 'file' && !pagedContents.length" class="empty-list-item">
              <template #prepend>
                <v-avatar size="42" class="me-2" color="grey-lighten-3" variant="tonal">
                  <v-icon color="grey">mdi-file-remove-outline</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>暂无可提取{{ moduleLabel }}内容</v-list-item-title>
              <v-list-item-subtitle>当前文件中未识别到该类型条目</v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <div class="d-flex justify-center py-3" v-if="pageCount > 1">
            <v-pagination v-model="listPage" :length="pageCount" :total-visible="5" density="comfortable"></v-pagination>
          </div>
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="8" class="preview-section pa-0" :class="{ 'full-height-panel': !compactMode }">
      <v-card :style="previewCardStyle">
        <v-card-text class="content-preview" :style="previewBodyStyle">
          <template v-if="previewMode === 'file' && previewUrl && previewCanInline">
            <div class="text-h6 mb-2">{{ previewFileName || `${moduleLabel}文件预览` }}</div>
            <div class="text-body-2 text-grey mb-3">
              已切换为文件预览模式{{ previewFileExt ? `（${previewFileExt.toUpperCase()}）` : '' }}
            </div>
            <iframe
              class="file-preview-frame"
              :src="previewUrl"
              title="file-preview"
            ></iframe>
            <div class="mt-3 text-caption text-grey">
              若当前浏览器不支持内嵌预览，请
              <a :href="previewUrl" target="_blank" rel="noopener">在新窗口打开</a>
            </div>
          </template>

          <template v-else-if="previewMode === 'file' && previewUrl && !previewCanInline">
            <div class="text-h6 mb-2">{{ previewFileName || `${moduleLabel}文件预览` }}</div>
            <div class="text-body-2 text-grey mb-3">
              当前文件类型{{ previewFileExt ? `（${previewFileExt.toUpperCase()}）` : '' }}暂不支持页面内预览。
            </div>
            <v-alert type="info" variant="tonal" class="mb-3">
              已避免自动下载。你可以手动选择下载后查看，或后续转换为 PDF 再预览。
            </v-alert>
            <v-btn color="primary" variant="tonal" :href="buildOriginalDownloadUrl(previewUrl)" target="_blank" rel="noopener">
              手动下载/打开原文件
            </v-btn>
          </template>

          <template v-else-if="activeItem">
            <div class="text-h6 mb-2">{{ activeItem.title || `${moduleLabel}内容预览` }}</div>
            <div class="text-body-2 text-grey mb-4">{{ activeItem.source || '提取内容' }}</div>
            <div class="text-body-2 content-text">{{ activeItem.text }}</div>
          </template>
          <div v-else class="d-flex align-center justify-center fill-height">
            <div class="text-h6 text-grey">请选择一条{{ moduleLabel }}内容查看详情</div>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import uploadApi from '@/api/upload'
import { useSnackbarStore } from '@/stores/snackbar'

interface ExtractedContent {
  content_id: number
  title: string
  text: string
  source: string
}

interface PreviewFileItem {
  file_id: number
  file_name: string
  file_ext: string
  preview_url: string
  can_inline: boolean
}

type PreviewMode = 'text' | 'file' | 'none'

const props = withDefaults(defineProps<{
  fileId?: number | string
  fileIds?: number[]
  contentType: 'paper' | 'review'
  moduleLabel: string
  showMetaControls?: boolean
}>(), {
  fileId: '',
  fileIds: () => [],
  showMetaControls: true
})

const emit = defineEmits<{
  (e: 'tagChanged', tag: string): void
  (e: 'addName', name: string): void
}>()

const snackbar = useSnackbarStore()
const taskName = ref('')
const selectedTag = ref<string | null>(null)
const contents = ref<ExtractedContent[]>([])
const activeItem = ref<ExtractedContent | null>(null)
const previewMode = ref<PreviewMode>('text')
const previewUrl = ref('')
const previewFileName = ref('')
const previewFileExt = ref('')
const previewCanInline = ref(true)
const previewFiles = ref<PreviewFileItem[]>([])
const activePreviewFileId = ref<number | null>(null)
// 多材料复用时隐藏顶部输入区，启用紧凑模式
const compactMode = computed(() => !props.showMetaControls)

// 列表分页：每页最多展示5条
const itemsPerPage = 5
const listPage = ref(1)
const pageCount = computed(() => Math.max(1, Math.ceil(contents.value.length / itemsPerPage)))
const pagedContents = computed(() => {
  const start = (listPage.value - 1) * itemsPerPage
  return contents.value.slice(start, start + itemsPerPage)
})

// 紧凑模式下根据当前页条目数动态调整卡片高度
const visibleItemCount = computed(() => Math.max(1, Math.min(pagedContents.value.length, itemsPerPage)))
const listBodyStyle = computed(() => {
  if (!compactMode.value) {
    return {}
  }
  return {
    maxHeight: `${visibleItemCount.value * 84}px`
  }
})

const contentScrollStyle = computed(() => {
  const overflowY = pagedContents.value.length > 0 ? 'auto' : 'hidden'
  return {
    overflowY: overflowY as 'auto' | 'hidden'
  }
})

const listCardStyle = computed(() => {
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
    minHeight: activeItem.value ? '320px' : `${visibleItemCount.value * 84}px`
  }
})

const previewCardStyle = computed(() => {
  if (!compactMode.value) {
    return {}
  }
  return {
    minHeight: activeItem.value ? '320px' : `${visibleItemCount.value * 84}px`
  }
})

const moduleIcon = computed(() => (props.contentType === 'paper' ? 'mdi-file-document-outline' : 'mdi-file-search-outline'))

const mappedTag = [
  { title: '医学', value: 'Medicine' },
  { title: '生物', value: 'Biology' },
  { title: '化学', value: 'Chemistry' },
  { title: '图形学', value: 'Graphics' },
  { title: '其他', value: 'Other' }
]

const emitTaskName = () => {
  emit('addName', taskName.value)
}

const selectItem = (item: ExtractedContent) => {
  activeItem.value = item
}

const selectPreviewFile = (item: PreviewFileItem) => {
  activePreviewFileId.value = item.file_id
  previewFileName.value = item.file_name
  previewFileExt.value = item.file_ext
  previewUrl.value = item.preview_url
  previewCanInline.value = item.can_inline
}

const normalizeItems = (raw: any): ExtractedContent[] => {
  // 兼容后端不同字段命名，统一映射到前端展示结构
  const sourceList = raw?.contents || raw?.results || raw?.items || []
  if (!Array.isArray(sourceList)) {
    return []
  }

  return sourceList.map((item: any, index: number) => ({
    content_id: Number(item.content_id ?? item.id ?? index + 1),
    title: String(item.title ?? item.name ?? `${props.moduleLabel}片段${index + 1}`),
    text: String(item.text ?? item.content ?? item.summary ?? '暂无提取内容'),
    source: String(item.source ?? item.source_type ?? '提取内容')
  }))
}

const appendPreviewToken = (url: string): string => {
  if (!url || !url.includes('/api/')) {
    return url
  }

  const token = localStorage.getItem('2-token')
  if (!token) {
    return url
  }

  const sep = url.includes('?') ? '&' : '?'
  return `${url}${sep}token=${encodeURIComponent(token)}`
}

const buildOriginalDownloadUrl = (url: string): string => {
  if (!url) {
    return ''
  }
  const sep = url.includes('?') ? '&' : '?'
  return `${url}${sep}download=1`
}

const loadContents = async () => {
  const targetFileIds = props.fileIds.length
    ? props.fileIds
    : (props.fileId ? [Number(props.fileId)] : [])

  const normalizedTargetIds = targetFileIds
    .map(id => Number(id))
    .filter(id => Number.isFinite(id) && id > 0)

  if (!normalizedTargetIds.length) {
    return
  }

  try {
    const aggregatedTextItems: ExtractedContent[] = []
    const aggregatedPreviewFiles: PreviewFileItem[] = []
    let contentCounter = 1

    for (const fileId of normalizedTargetIds) {
      const response = (await uploadApi.getExtractedContents({
        file_id: fileId,
        content_type: props.contentType,
        page_number: 1,
        page_size: 50
      })).data

      const mode = (response?.preview_mode || 'text') as PreviewMode
      if (mode === 'file' && response?.preview_url) {
        aggregatedPreviewFiles.push({
          file_id: Number(response.file_id || fileId),
          file_name: String(response.file_name || `${props.moduleLabel}文件`),
          file_ext: String(response.file_ext || ''),
          preview_url: appendPreviewToken(String(response.preview_url)),
          can_inline: Boolean(response.can_inline)
        })
      }

      const normalizedItems = normalizeItems(response).map(item => ({
        ...item,
        content_id: contentCounter++
      }))
      aggregatedTextItems.push(...normalizedItems)
    }

    previewFiles.value = aggregatedPreviewFiles
    if (previewFiles.value.length > 0) {
      previewMode.value = 'file'
      selectPreviewFile(previewFiles.value[0])
    } else {
      previewMode.value = 'text'
      previewFileName.value = ''
      previewFileExt.value = ''
      previewUrl.value = ''
      previewCanInline.value = true
      activePreviewFileId.value = null
    }

    contents.value = aggregatedTextItems
    listPage.value = 1
    if (previewMode.value !== 'file' && !contents.value.length) {
      snackbar.showMessage(`当前文件暂无可展示的${props.moduleLabel}提取内容`, 'warning')
    }
    activeItem.value = previewMode.value === 'file' ? null : (compactMode.value ? null : (contents.value[0] || null))
  } catch (error) {
    contents.value = []
    previewFiles.value = []
    activeItem.value = null
    previewMode.value = 'none'
    previewUrl.value = ''
    previewCanInline.value = true
    activePreviewFileId.value = null
    snackbar.showMessage(`${props.moduleLabel}提取内容加载失败`, 'error')
  }
}

watch(selectedTag, (newVal) => {
  emit('tagChanged', newVal || '')
})

watch(contents, () => {
  // 列表总数变化时，自动修正越界页码
  if (listPage.value > pageCount.value) {
    listPage.value = pageCount.value
  }
}, { deep: true })

onMounted(() => {
  loadContents()
})

watch(
  () => [props.fileId, props.fileIds.join(',')],
  () => {
    loadContents()
  }
)
</script>

<style scoped>
.content-list {
  overflow: hidden;
}

.preview-section {
  overflow: hidden;
}

.full-height-panel {
  height: calc(100vh - 300px);
}

.content-scroll {
  overflow-y: hidden;
}

.v-list-item {
  min-height: 80px;
  padding: 8px 16px;
}

.empty-list-item {
  opacity: 0.9;
}

.selected-item {
  background-color: rgb(var(--v-theme-primary), 0.1);
}

.content-preview {
  min-height: 220px;
}

.content-text {
  white-space: pre-wrap;
  line-height: 1.6;
}

.file-preview-frame {
  width: 100%;
  min-height: 520px;
  border: 1px solid rgba(var(--v-theme-primary), 0.18);
  border-radius: 8px;
}
</style>

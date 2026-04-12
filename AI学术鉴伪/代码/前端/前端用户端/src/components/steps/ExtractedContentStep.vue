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
        <v-spacer />
        <v-btn color="primary" prepend-icon="mdi-check-all" @click="toggleAll">
          {{ isAllSelected ? '取消全选' : '全选' }}
        </v-btn>
      </div>
    </v-col>
  </v-row>

  <v-row>
    <v-col cols="4" class="content-list pa-0" :class="{ 'full-height-panel': !compactMode }">
      <v-card :style="listCardStyle">
        <v-card-text class="pa-0" :style="listBodyStyle">
          <v-list lines="two" class="content-scroll" :style="contentScrollStyle">
            <v-list-item
              v-for="(item, index) in pagedContents"
              :key="item.content_id"
              :class="{ 'selected-item': item.selected }"
              @click="selectItem(item)"
            >
              <template #prepend>
                <v-avatar size="42" class="me-2" color="primary" variant="tonal">
                  <v-icon>{{ moduleIcon }}</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>{{ item.title || `${moduleLabel}片段${index + 1}` }}</v-list-item-title>
              <v-list-item-subtitle>{{ item.source || '提取内容' }}</v-list-item-subtitle>
              <template #append>
                <v-checkbox
                  v-model="item.selected"
                  hide-details
                  density="compact"
                  @click.stop
                  @update:model-value="emitUpdate"
                />
              </template>
            </v-list-item>

            <v-list-item v-if="!pagedContents.length" class="empty-list-item">
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
          <template v-if="activeItem">
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
  selected: boolean
}

const props = withDefaults(defineProps<{
  fileId?: number | string
  contentType: 'paper' | 'review'
  moduleLabel: string
  showMetaControls?: boolean
}>(), {
  fileId: '',
  showMetaControls: true
})

const emit = defineEmits<{
  (e: 'update', selectedContents: ExtractedContent[]): void
  (e: 'tagChanged', tag: string): void
  (e: 'addName', name: string): void
}>()

const snackbar = useSnackbarStore()
const taskName = ref('')
const selectedTag = ref<string | null>(null)
const contents = ref<ExtractedContent[]>([])
const activeItem = ref<ExtractedContent | null>(null)
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
  return {
    overflowY: pagedContents.value.length > 0 ? 'auto' : 'hidden'
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
const isAllSelected = computed(() => contents.value.length > 0 && contents.value.every(item => item.selected))

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

const emitUpdate = () => {
  emit('update', contents.value.filter(item => item.selected))
}

const selectItem = (item: ExtractedContent) => {
  activeItem.value = item
}

const toggleAll = () => {
  const next = !isAllSelected.value
  contents.value.forEach(item => {
    item.selected = next
  })
  emitUpdate()
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
    source: String(item.source ?? item.source_type ?? '提取内容'),
    selected: false
  }))
}

const loadContents = async () => {
  if (!props.fileId) {
    return
  }

  try {
    // 获取论文/Review提取内容，并交给前端分页渲染
    const response = (await uploadApi.getExtractedContents({
      file_id: props.fileId,
      content_type: props.contentType,
      page_number: 1,
      page_size: 50
    })).data

    contents.value = normalizeItems(response)
    listPage.value = 1
    if (!contents.value.length) {
      snackbar.showMessage(`当前文件暂无可展示的${props.moduleLabel}提取内容`, 'warning')
    }
    activeItem.value = compactMode.value ? null : (contents.value[0] || null)
  } catch (error) {
    contents.value = []
    activeItem.value = null
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
</style>

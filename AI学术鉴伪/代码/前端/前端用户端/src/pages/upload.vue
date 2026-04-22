<template>
  <!-- 上传页面内容 -->
  <div v-show="!showProgress">
    <v-row>
      <v-col cols="12" lg="11">
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4 module-switcher">
              <div class="text-subtitle-1 font-weight-medium mb-3">检测模块</div>
              <div class="d-flex flex-wrap ga-3">
                <v-btn v-for="module in uploadModules" :key="module.key" :variant="selectedModule === module.key ? 'flat' : 'outlined'"
                  :color="selectedModule === module.key ? 'primary' : 'default'" @click="handleModuleChange(module.key)">
                  {{ module.label }}
                </v-btn>
              </div>
              <div class="text-caption text-grey mt-3">
                {{ currentModule.hint }}
              </div>
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="4">
            <v-card class="h-100" :class="{ 'border border-primary': selectedVersion === 1 }"
              @click="selectedVersion = 1">
              <v-card-title class="text-h6">基础版</v-card-title>
              <v-card-subtitle>0元/张</v-card-subtitle>
              <v-card-text>
                <div class="text-body-2 mb-4">适用于个人{{ currentModule.label }}任务</div>
                <v-list density="compact">
                  <v-list-item>
                    <template v-slot:prepend>
                      <div class="text-primary">AI模型</div>
                    </template>
                    <template v-slot:append>
                      <div class="text-primary">基础版</div>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>支持格式</div>
                    </template>
                    <template v-slot:append>
                      <div class="text-warning">{{ currentModule.basicFormat }}</div>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>免费额度</div>
                    </template>
                    <template v-slot:append>
                      <div class="text-warning">每天5张</div>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>检测精度</div>
                    </template>
                    <template v-slot:append>
                      <v-icon color="warning">mdi-star</v-icon>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="h-100" :class="{ 'border border-primary': selectedVersion === 2 }"
              @click="selectedVersion = 2">
              <v-card-title class="text-h6">专业版</v-card-title>
              <v-card-subtitle>1元/张</v-card-subtitle>
              <v-card-text>
                <div class="text-body-2 mb-4">适用于批量{{ currentModule.label }}任务</div>
                <v-list density="compact">
                  <v-list-item>
                    <template v-slot:prepend>
                      <div class="text-primary">AI模型</div>
                    </template>
                    <template v-slot:append>
                      <div class="text-primary">专业版</div>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>支持格式</div>
                    </template>
                    <template v-slot:append>
                      <div class="text-warning">{{ currentModule.proFormat }}</div>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>极速检测</div>
                    </template>
                    <template v-slot:append>
                      <v-icon color="success">mdi-check</v-icon>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>检测精度</div>
                    </template>
                    <template v-slot:append>
                      <div class="d-flex">
                        <v-icon color="warning">mdi-star</v-icon>
                        <v-icon color="warning">mdi-star</v-icon>
                      </div>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="h-100" :class="{ 'border border-primary': selectedVersion === 3 }"
              @click="selectedVersion = 3">
              <v-card-title class="text-h6">至尊版</v-card-title>
              <v-card-subtitle>定制价格</v-card-subtitle>
              <v-card-text>
                <div class="text-body-2 mb-4">适用于复杂{{ currentModule.label }}任务</div>
                <v-list density="compact">
                  <v-list-item>
                    <template v-slot:prepend>
                      <div class="text-primary">AI模型</div>
                    </template>
                    <template v-slot:append>
                      <div class="text-primary">尊贵定制</div>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>支持格式</div>
                    </template>
                    <template v-slot:append>
                      <div class="text-warning">{{ currentModule.proFormat }}</div>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>检测极速</div>
                    </template>
                    <template v-slot:append>
                      <v-icon color="success">mdi-check</v-icon>
                      <v-icon color="success">mdi-check</v-icon>
                    </template>
                  </v-list-item>
                  <v-list-item>
                    <template v-slot:prepend>
                      <div>检测精度</div>
                    </template>
                    <template v-slot:append>
                      <div class="d-flex">
                        <v-icon color="warning">mdi-star</v-icon>
                        <v-icon color="warning">mdi-star</v-icon>
                        <v-icon color="warning">mdi-star</v-icon>
                      </div>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row class="mt-6">
          <v-col cols="12">
            <v-card>
              <v-card-text class="text-center">
                <div v-if="!selectedFiles.length" class="upload-area pa-8" @dragover.prevent @drop.prevent="handleDrop"
                  @click="triggerFileInput">
                  <v-icon size="64" color="grey">mdi-cloud-upload</v-icon>
                  <div class="text-h6 mt-4">点击或拖拽{{ currentModule.label }}文件到此处上传</div>
                  <div class="text-caption text-grey">支持格式：{{ currentModule.acceptText }}，单个文件不超过{{ currentModule.maxSizeMB }}MB</div>
                  <input type="file" ref="fileInput" style="display: none" @change="handleFileSelect"
                    :accept="currentModule.acceptAttr" multiple>
                </div>
                <div v-else class="file-preview pa-4">
                  <div class="text-subtitle-1 mb-3">已选择 {{ selectedFiles.length }} 个文件</div>
                  <v-row>
                    <v-col v-for="(file, index) in selectedFiles" :key="`${file.name}-${file.lastModified}`" cols="12" md="6">
                      <v-card class="h-100">
                        <v-card-text class="d-flex align-center">
                          <v-icon size="48" color="primary" class="mr-4">mdi-file</v-icon>
                          <div>
                            <div class="text-h6">{{ file.name }}</div>
                            <div class="text-caption text-grey">
                              {{ formatFileSize(file.size) }}
                            </div>
                          </div>
                          <v-spacer></v-spacer>
                          <v-btn icon="mdi-close" variant="text" @click="removeSelectedFile(index)"></v-btn>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                  <div class="d-flex justify-end mt-2">
                    <v-btn variant="text" color="error" @click="selectedFiles = []">清空全部</v-btn>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row class="mt-4">
          <v-col cols="12" class="d-flex justify-end">
            <v-btn color="primary" size="large" :loading="loading" @click="handleSubmit">
              {{ loading ? '处理中...' : actionButtonText }}
              <template v-slot:loader>
                <v-progress-circular indeterminate color="white" size="24"></v-progress-circular>
              </template>
              <v-icon v-if="!loading" end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-col>

      <!-- <v-col cols="12" lg="3">
        <v-card>
          <v-card-title class="d-flex align-center">
            实时检测动态
            <v-spacer></v-spacer>
            <v-btn icon="mdi-chevron-left" variant="text" density="compact"></v-btn>
            <v-btn icon="mdi-chevron-right" variant="text" density="compact"></v-btn>
          </v-card-title>
          <v-card-text>
            <v-timeline density="compact" align="start">
              <v-timeline-item v-for="(item, index) in timelineItems" :key="index" dot-color="primary" size="small">
                <div class="d-flex align-center">
                  <v-avatar size="32" class="mr-3">
                    <v-img :src="item.avatar" cover></v-img>
                  </v-avatar>
                  <div>
                    <div class="d-flex align-center">
                      <span class="text-body-2">{{ item.name }}</span>
                      <v-chip size="x-small" :color="item.tagColor" class="ml-2" label>{{ item.tag }}</v-chip>
                    </div>
                    <div class="text-caption text-grey">
                      {{ item.count }}张图片 平均造假率: {{ item.rate }}
                    </div>
                  </div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col> -->
    </v-row>
  </div>

  <!-- 进度页面内容 -->
  <div v-show="showProgress" class="upload-progress">
    <!-- 返回按钮 -->
    <div class="d-flex align-center mb-6">
      <v-btn icon="mdi-arrow-left" variant="text" @click="returnToUpload" class="mr-2 return-btn">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <span class="text-h6 font-weight-medium">返回上传</span>
      <v-chip class="ml-3" color="primary" variant="tonal">{{ currentModule.label }}</v-chip>
    </div>

    <v-card>
      <v-card-text>
        <ImageSelectionStep
          v-if="fileId && selectedModule === 'image'"
          :fileId="fileId"
          @tagChanged="handleSelectedTag"
          @add-name="handleName"
        />

        <ExtractedContentStep
          v-if="fileId && selectedModule === 'paper'"
          :fileId="fileId"
          contentType="paper"
          moduleLabel="论文"
          @tagChanged="handleSelectedTag"
          @add-name="handleName"
        />

        <ExtractedContentStep
          v-if="fileId && selectedModule === 'review'"
          :fileId="fileId"
          contentType="review"
          moduleLabel="Review"
          @tagChanged="handleSelectedTag"
          @add-name="handleName"
        />

        <div v-if="fileId && selectedModule === 'multi'">
          <v-row>
            <v-col cols="6" class="mb-2">
              <v-select
                v-model="currentTag"
                :items="mappedTag"
                label="为多材料任务添加标签"
                clearable
                variant="outlined"
                hide-details
              />
            </v-col>
            <v-col cols="6" class="mb-2">
              <v-text-field
                v-model="currentTaskName"
                label="为该检测任务添加名称"
                variant="outlined"
                :rules="[v => !v || v.length <= 10 || '任务名称不能超过10个字']"
                counter="10"
              />
            </v-col>
          </v-row>

          <v-card variant="outlined" class="mb-4">
            <v-card-title class="text-subtitle-1">图片内容</v-card-title>
            <v-card-text>
              <ImageSelectionStep
                :fileId="fileId"
                :showMetaControls="false"
              />
            </v-card-text>
          </v-card>

          <v-card variant="outlined" class="mb-4">
            <v-card-title class="text-subtitle-1">论文内容</v-card-title>
            <v-card-text>
              <ExtractedContentStep
                :fileId="fileId"
                contentType="paper"
                moduleLabel="论文"
                :showMetaControls="false"
              />
            </v-card-text>
          </v-card>

          <v-card variant="outlined">
            <v-card-title class="text-subtitle-1">Review内容</v-card-title>
            <v-card-text>
              <ExtractedContentStep
                :fileId="fileId"
                contentType="review"
                moduleLabel="Review"
                :showMetaControls="false"
              />
            </v-card-text>
          </v-card>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="elevated" @click="handleNext" :disabled="!canProceed"
          append-icon="mdi-arrow-right">
          启动检测
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import uploadApi from '@/api/upload'
import { useSnackbarStore } from '@/stores/snackbar'
import ImageSelectionStep from '@/components/steps/ImageSelectionStep.vue'
import ExtractedContentStep from '@/components/steps/ExtractedContentStep.vue'
import publisher from '@/api/publisher'
import axios from 'axios'

const router = useRouter()
const selectedVersion = ref<1 | 2 | 3 | null>(null)
type ModuleKey = 'image' | 'paper' | 'review' | 'multi'

interface UploadModule {
  key: ModuleKey
  label: string
  hint: string
  acceptText: string
  acceptAttr: string
  basicFormat: string
  proFormat: string
  allowedExtensions: string[]
  maxSizeMB: number
}

const uploadModules: UploadModule[] = [
  {
    key: 'image',
    label: '图片检测',
    hint: '适用于单图或图集的AI造假识别。',
    acceptText: 'JPG、JPEG、PNG、PDF、ZIP',
    acceptAttr: '.jpg,.jpeg,.png,.pdf,.zip',
    basicFormat: 'JPG/PNG',
    proFormat: 'JPG/PNG/PDF/ZIP',
    allowedExtensions: ['jpg', 'jpeg', 'png', 'pdf', 'zip'],
    maxSizeMB: 100
  },
  {
    key: 'paper',
    label: '论文检测',
    hint: '适用于论文文档中的图文一致性与可疑内容分析。',
    acceptText: 'PDF、DOC、DOCX、TXT、ZIP',
    acceptAttr: '.pdf,.doc,.docx,.txt,.zip',
    basicFormat: 'PDF/DOCX',
    proFormat: 'PDF/DOC/DOCX/TXT/ZIP',
    allowedExtensions: ['pdf', 'doc', 'docx', 'txt', 'zip'],
    maxSizeMB: 100
  },
  {
    key: 'review',
    label: 'Review检测',
    hint: '适用于审稿材料的Review质量与引用风险辅助评估。',
    acceptText: 'PDF、DOC、DOCX、TXT、ZIP',
    acceptAttr: '.pdf,.doc,.docx,.txt,.zip',
    basicFormat: 'PDF/TXT',
    proFormat: 'PDF/DOC/DOCX/TXT/ZIP',
    allowedExtensions: ['pdf', 'doc', 'docx', 'txt', 'zip'],
    maxSizeMB: 100
  },
  {
    key: 'multi',
    label: '多材料综合检测',
    hint: '适用于图片、论文、补充材料联合分析。',
    acceptText: 'JPG、JPEG、PNG、PDF、DOC、DOCX、TXT、ZIP',
    acceptAttr: '.jpg,.jpeg,.png,.pdf,.doc,.docx,.txt,.zip',
    basicFormat: 'JPG/PDF/DOCX',
    proFormat: '全格式',
    allowedExtensions: ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx', 'txt', 'zip'],
    maxSizeMB: 100
  }
]

const selectedModule = ref<ModuleKey>('image')
const currentModule = computed(() => uploadModules.find(module => module.key === selectedModule.value) ?? uploadModules[0])

const fileInput = ref<HTMLInputElement | null>(null)
const selectedFiles = ref<File[]>([])
const fileId = ref()
const loading = ref<boolean>(false)
const snackbar = useSnackbarStore()

// 进度页面相关状态
const showProgress = ref(false)
const currentTag = ref<string>('')
const currentTaskName = ref('')

const mappedTag = [
  { title: '医学', value: 'Medicine' },
  { title: '生物', value: 'Biology' },
  { title: '化学', value: 'Chemistry' },
  { title: '图形学', value: 'Graphics' },
  { title: '其他', value: 'Other' }
]

const actionButtonText = computed(() => {
  return '校验上传内容'
})

const resetCurrentUploadState = () => {
  selectedFiles.value = []
  selectedVersion.value = null
  fileId.value = ''
  currentTag.value = ''
  currentTaskName.value = ''
}

const handleModuleChange = (moduleKey: ModuleKey) => {
  if (selectedModule.value === moduleKey) {
    return
  }
  selectedModule.value = moduleKey
  resetCurrentUploadState()
}

const getFileExtension = (fileName: string): string => {
  const segments = fileName.split('.')
  if (segments.length <= 1) {
    return ''
  }
  return segments[segments.length - 1].toLowerCase()
}

const processIncomingFiles = (files: File[]) => {
  const validFiles: File[] = []
  const invalidFiles: File[] = []

  files.forEach(file => {
    if (isValidFile(file)) {
      validFiles.push(file)
    } else {
      invalidFiles.push(file)
    }
  })

  if (validFiles.length > 0) {
    selectedFiles.value = validFiles
  }

  if (invalidFiles.length > 0) {
    snackbar.showMessage(
      `有 ${invalidFiles.length} 个文件格式不支持或超过 ${currentModule.value.maxSizeMB}MB，已自动忽略`,
      'warning'
    )
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    processIncomingFiles(Array.from(files))
  }
}

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  const files = input.files
  if (files && files.length > 0) {
    processIncomingFiles(Array.from(files))
  }
  input.value = ''
}

const removeSelectedFile = (index: number) => {
  selectedFiles.value.splice(index, 1)
}

const handleName = async (newName: string) => {
  console.log(newName)
  currentTaskName.value = newName
}

const handleSelectedTag = async (newTag: string) => {
  console.log(newTag)
  currentTag.value = newTag
}

const isValidFile = (file: File): boolean => {
  const extension = getFileExtension(file.name)
  const maxSize = currentModule.value.maxSizeMB * 1024 * 1024
  return currentModule.value.allowedExtensions.includes(extension) && file.size <= maxSize
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const handleSubmit = async () => {
  if (!selectedVersion.value) {
    snackbar.showMessage('请选择检测版本', 'error')
    return
  }

  if (!selectedFiles.value.length) {
    snackbar.showMessage('请选择要上传的文件', 'error')
    return
  }

  loading.value = true
  try {
    const formData = new FormData()
    selectedFiles.value.forEach(file => {
      formData.append('file', file)
    })
    formData.append('detect_type', selectedModule.value)
    const { data } = await uploadApi.uploadFile(formData)
    fileId.value = data.file_id
    snackbar.showMessage('文件上传成功，正在处理中...', 'success')

    // 获取提取的图片
    // const { data: imagesData } = await uploadApi.getExtractedImages(data.file_id)
    // extractedImages.value = imagesData.images.map((img: any) => ({
    //   image_id: img.image_id,
    //   image_url: import.meta.env.VITE_API_URL + img.image_url,
    //   page_number: img.page_number,
    //   extracted_from_pdf: img.extracted_from_pdf,
    //   selected: false
    // }))

    // 显示进度页面
    showProgress.value = true
  } catch (error: any) {
    let message = '提交图片失败'
    if (axios.isAxiosError(error)) {
      const status = error?.code
      if (status === 'ERR_NETWORK') {
        message = '用户无权限'
      }
    }
    snackbar.showMessage(message, 'error')
  } finally {
    loading.value = false
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

// 进度页面相关方法
const canProceed = computed(() => {
  return !!fileId.value && (!currentTaskName.value || currentTaskName.value.length <= 10)
})

const handleTag = async (tag: string) => {
  if (!tag) {
    return
  }

  console.log('parent: ' + tag)
  try {
    await uploadApi.addTag({ fileId: fileId.value, tag })
    console.log('标签已保存')
  } catch (error) {
    console.error('保存失败:', error)
    snackbar.showMessage('标签无效', 'error')
  }
}

const handleNext = async () => {
  await handleTag(currentTag.value)
  if (canProceed.value) {
    try {
      const normalizedFileId = Number(fileId.value)
      if (!Number.isFinite(normalizedFileId) || normalizedFileId <= 0) {
        snackbar.showMessage('文件ID无效，请重新上传', 'error')
        return
      }

      const payload: Record<string, any> = {
        image_ids: [normalizedFileId],
        task_name: currentTaskName.value,
        mode: selectedVersion.value,
        detect_type: selectedModule.value
      }

      await publisher.submitDetection(payload)
      router.push(`/history`)
    } catch (error: any) {
      const message = error?.response?.data?.message || '图片上传失败'
      snackbar.showMessage(message, 'error')
    }
  }
}

// 添加返回上传页面的方法
const returnToUpload = () => {
  showProgress.value = false
  resetCurrentUploadState()
}
</script>

<style scoped>
.module-switcher {
  border: 1px solid rgba(var(--v-theme-primary), 0.12);
  border-radius: 12px;
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-area:hover {
  border-color: var(--v-primary-base);
  background-color: rgba(var(--v-primary-base), 0.05);
}

.border {
  border-width: 2px !important;
  border-style: solid !important;
}

.border-primary {
  border-color: rgb(var(--v-theme-primary)) !important;
}

.v-timeline-item {
  margin-bottom: 16px;
}

.v-timeline-item:last-child {
  margin-bottom: 0;
}

.file-preview {
  border: 2px solid rgb(var(--v-theme-primary));
  border-radius: 8px;
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.v-btn--loading {
  opacity: 1;
}

.upload-progress {
  position: relative;
  min-height: 100vh;
  max-height: 300vh;
  background-color: rgb(var(--v-theme-surface));
  overflow: hidden;
}

.v-stepper {
  box-shadow: none;
}
</style>
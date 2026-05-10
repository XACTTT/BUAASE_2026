<!-- eslint-disable -->
<template>
  <v-container fluid class="model-chat-test-page">
    <v-row class="mb-6 align-center">
      <v-col cols="12" md="8">
        <div class="d-flex flex-column gap-2">
          <div class="d-flex align-center flex-wrap gap-3">
            <h1 class="text-h4 font-weight-bold">模型对话测试</h1>
            <v-chip variant="tonal" size="small" color="warning">临时工具</v-chip>
          </div>
          <p class="text-body-2 text-medium-emphasis">
            用于手工测试模型调用与结构化输出。不会影响检测任务流程。
          </p>
        </div>
      </v-col>
    </v-row>

    <v-card rounded="xl" elevation="2">
      <v-card-text>
        <v-row dense>
          <v-col cols="12" md="5">
            <v-select
              v-model="selectedSourceId"
              :items="sourceOptions"
              item-title="title"
              item-value="value"
              label="模型源"
              variant="outlined"
              density="compact"
              @update:modelValue="handleSourceChange"
            />
          </v-col>
          <v-col cols="12" md="7">
            <v-select
              v-model="selectedModelConfigId"
              :items="modelOptions"
              item-title="title"
              item-value="value"
              label="模型配置"
              variant="outlined"
              density="compact"
            />
          </v-col>

          <v-col cols="12" md="4">
            <v-text-field
              v-model="chatForm.taskId"
              label="task_id (可选)"
              variant="outlined"
              density="compact"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="chatForm.stage"
              :items="stageOptions"
              label="stage (可选)"
              variant="outlined"
              density="compact"
              clearable
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="chatForm.responseFormat"
              label="response_format (可选)"
              hint="json_object 或 {&quot;type&quot;:&quot;json_object&quot;}"
              persistent-hint
              variant="outlined"
              density="compact"
            />
          </v-col>
          <v-col cols="12" md="8">
            <v-file-input
              v-model="uploadFiles"
              label="上传文件 (可选)"
              variant="outlined"
              density="compact"
              multiple
              clearable
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-btn
              color="secondary"
              variant="tonal"
              :loading="uploadLoading"
              :disabled="!uploadFiles.length"
              @click="submitUploadFiles"
            >
              上传文件
            </v-btn>
          </v-col>
          <v-col cols="12" md="8" v-if="uploadedFiles.length">
            <v-text-field
              :model-value="uploadedFiles.map((item) => item.file_token).join(', ')"
              label="已上传 file_token"
              variant="outlined"
              density="compact"
              readonly
            />
          </v-col>

          <v-col cols="12">
            <v-text-field
              v-model="chatForm.prompt"
              label="prompt (可选)"
              variant="outlined"
              density="compact"
            />
          </v-col>

          <v-col cols="12" md="6">
            <v-textarea
              v-model="chatForm.messagesText"
              label="messages (JSON)"
              rows="12"
              variant="outlined"
              density="compact"
              readonly
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-textarea
              v-model="chatForm.inputPayloadText"
              label="input_payload (JSON, 可选)"
              rows="12"
              variant="outlined"
              density="compact"
            />
          </v-col>

          <v-col cols="12">
            <v-textarea
              v-model="chatResponse"
              label="响应"
              rows="10"
              variant="outlined"
              density="compact"
              readonly
            />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="px-6 pb-6">
        <v-spacer></v-spacer>
        <v-btn variant="text" color="grey" @click="resetForm">重置</v-btn>
        <v-btn color="primary" :loading="chatLoading" @click="submitChatTest">发送测试</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import modelApi, { type ChatModelPayload, type ModelSourceEntity } from '@/api/model'
import chatTestUploadApi from '@/api/chat-test-upload'
import { useSnackbarStore } from '@/stores/snackbar'
import { useUserStore } from '@/stores/user'

const snackbar = useSnackbarStore()
const userStore = useUserStore()

const sources = ref<ModelSourceEntity[]>([])
const selectedSourceId = ref<number | null>(null)
const selectedModelConfigId = ref<number | null>(null)
const chatLoading = ref(false)
const chatResponse = ref('')
const uploadLoading = ref(false)
const uploadFiles = ref<File[]>([])
const uploadedFiles = ref<Array<{ file_token: string; file_name: string; file_url?: string; size?: number }>>([])

const defaultMessages = [
  { role: 'system', content: '你是学术鉴伪分析助手，请输出 JSON 结构。' },
  { role: 'user', content: '请根据 input_payload 输出分析结果。' }
]

const stageMessageTemplates: Record<string, Array<{ role: string; content: string }>> = {
  paper: [
    { role: 'system', content: '你是学术鉴伪分析助手，当前任务为论文分析。输出结构化 JSON。' },
    { role: 'user', content: '请根据 input_payload 输出论文分析结果。' }
  ],
  review: [
    { role: 'system', content: '你是学术鉴伪分析助手，当前任务为评审分析。输出结构化 JSON。' },
    { role: 'user', content: '请根据 input_payload 输出评审分析结果。' }
  ],
  image: [
    { role: 'system', content: '你是图像鉴伪分析助手，当前任务为图像分析。输出结构化 JSON。' },
    { role: 'user', content: '请根据 input_payload 输出图像分析结果。' }
  ],
  multi_material: [
    { role: 'system', content: '你是学术鉴伪分析助手，当前任务为多材料综合分析。输出结构化 JSON。' },
    { role: 'user', content: '请根据 input_payload 输出综合分析结果。' }
  ],
  merge: [
    { role: 'system', content: '你是学术鉴伪分析助手，当前任务为多阶段汇总。输出结构化 JSON。' },
    { role: 'user', content: '请根据 input_payload 输出汇总结果。' }
  ]
}

const chatForm = ref({
  taskId: '',
  stage: '',
  prompt: '',
  messagesText: JSON.stringify(defaultMessages, null, 2),
  inputPayloadText: '{\n  "notes": ""\n}',
  responseFormat: 'json_object'
})

const selectedSource = computed(() => sources.value.find((source) => source.id === selectedSourceId.value) ?? null)

const stageOptions = [
  { title: '论文分析', value: 'paper' },
  { title: '评审分析', value: 'review' },
  { title: '图像分析', value: 'image' },
  { title: '多材料综合', value: 'multi_material' },
  { title: '汇总', value: 'merge' },
]

const sourceOptions = computed(() => {
  return sources.value.map((source) => ({
    title: `${source.name} (${source.vendor})`,
    value: source.id,
  }))
})

const modelOptions = computed(() => {
  if (!selectedSource.value) return []
  return selectedSource.value.models.map((model) => ({
    title: `${model.displayName} (${model.modelId})`,
    value: model.id,
  }))
})

watch(
  () => chatForm.value.stage,
  (stage) => {
    const template = stage ? stageMessageTemplates[stage] : null
    const messages = template ?? defaultMessages
    chatForm.value.messagesText = JSON.stringify(messages, null, 2)
  }
)

onMounted(async () => {
  if (!userStore.isLoaded) {
    await userStore.fetchUserInfo()
  }
  await loadSources()
})

async function loadSources() {
  try {
    const response = await modelApi.listAIModels()
    sources.value = response.data.sources || []
    if (sources.value.length) {
      selectedSourceId.value = sources.value[0].id
      selectedModelConfigId.value = sources.value[0].models[0]?.id ?? null
    }
  } catch (error) {
    void error
    snackbar.showMessage('加载模型源失败', 'error')
  }
}

function handleSourceChange() {
  selectedModelConfigId.value = selectedSource.value?.models[0]?.id ?? null
}

function resetForm() {
  chatForm.value = {
    taskId: '',
    stage: '',
    prompt: '',
    messagesText: JSON.stringify(defaultMessages, null, 2),
    inputPayloadText: '{\n  "notes": ""\n}',
    responseFormat: 'json_object'
  }
  chatResponse.value = ''
  uploadFiles.value = []
  uploadedFiles.value = []
}

function parseJsonOrNotify(label: string, raw: string) {
  try {
    return JSON.parse(raw)
  } catch (error) {
    void error
    snackbar.showMessage(`${label} 不是合法 JSON`, 'error')
    throw error
  }
}

async function submitChatTest() {
  if (!selectedModelConfigId.value) {
    snackbar.showMessage('请选择模型配置', 'warning')
    return
  }

  let messages: unknown
  let inputPayload: unknown
  try {
    messages = parseJsonOrNotify('messages', chatForm.value.messagesText)
    if (chatForm.value.inputPayloadText.trim()) {
      inputPayload = parseJsonOrNotify('input_payload', chatForm.value.inputPayloadText)
    }
  } catch (error) {
    void error
    return
  }

  if (!Array.isArray(messages)) {
    snackbar.showMessage('messages 必须是数组', 'error')
    return
  }

  let responseFormat: string | { type: string } | undefined
  const responseFormatRaw = chatForm.value.responseFormat.trim()
  if (responseFormatRaw) {
    if (responseFormatRaw.startsWith('{')) {
      try {
        responseFormat = parseJsonOrNotify('response_format', responseFormatRaw)
      } catch (error) {
        void error
        return
      }
    } else {
      responseFormat = responseFormatRaw
    }
  }

  const payload: ChatModelPayload = {
    model_config_id: selectedModelConfigId.value,
    messages: messages as ChatModelPayload['messages'],
  }

  const taskIdValue = chatForm.value.taskId.trim()
  if (taskIdValue) {
    const parsedTaskId = Number(taskIdValue)
    if (Number.isNaN(parsedTaskId)) {
      snackbar.showMessage('task_id 必须是数字', 'error')
      return
    }
    payload.task_id = parsedTaskId
  }

  if (chatForm.value.stage.trim()) {
    payload.stage = chatForm.value.stage.trim()
  }
  if (chatForm.value.prompt.trim()) {
    payload.prompt = chatForm.value.prompt.trim()
  }
  if (inputPayload && typeof inputPayload === 'object') {
    const mergedPayload = { ...(inputPayload as Record<string, unknown>) }
    if (uploadedFiles.value.length) {
      mergedPayload.file_tokens = uploadedFiles.value.map((item) => item.file_token)
      mergedPayload.files = uploadedFiles.value
    }
    payload.input_payload = mergedPayload
  } else if (uploadedFiles.value.length) {
    payload.input_payload = {
      file_tokens: uploadedFiles.value.map((item) => item.file_token),
      files: uploadedFiles.value,
    }
  }
  if (responseFormat) {
    payload.response_format = responseFormat
  }

  chatLoading.value = true
  try {
    const sourceTimeoutSec = selectedSource.value?.timeout ?? 30
    const timeoutMs = sourceTimeoutSec * 1000
    const response = await modelApi.chatWithModel(payload, timeoutMs)
    chatResponse.value = JSON.stringify(response.data, null, 2)
    snackbar.showMessage('对话测试完成', 'success')
  } catch (error) {
    void error
    snackbar.showMessage('对话测试失败', 'error')
  } finally {
    chatLoading.value = false
  }
}

async function submitUploadFiles() {
  if (!uploadFiles.value.length) return
  const formData = new FormData()
  uploadFiles.value.forEach((file) => {
    formData.append('file', file)
  })

  uploadLoading.value = true
    try {
      const response = await chatTestUploadApi.uploadTestFiles(formData)
      const files = response.data?.files as Array<{ file_token: string; file_name: string; file_url?: string; size?: number }> | undefined
      if (files?.length) {
        const merged = [...uploadedFiles.value, ...files]
        const map = new Map<string, { file_token: string; file_name: string; file_url?: string; size?: number }>()
        merged.forEach((f) => {
          if (f && f.file_token) map.set(f.file_token, f)
        })
        uploadedFiles.value = Array.from(map.values())
        snackbar.showMessage('文件上传成功', 'success')
        uploadFiles.value = []
        return
      }
      if (response.data?.file_token) {
        const fileObj = {
          file_token: response.data.file_token,
          file_name: response.data.file_name,
          file_url: response.data.file_url,
          size: response.data.size,
        }
        if (!uploadedFiles.value.find((f) => f.file_token === fileObj.file_token)) {
          uploadedFiles.value.push(fileObj)
        }
        snackbar.showMessage('文件上传成功', 'success')
        uploadFiles.value = []
        return
      }
      snackbar.showMessage('文件上传成功', 'success')
    } catch (error) {
    void error
    snackbar.showMessage('文件上传失败', 'error')
  } finally {
    uploadLoading.value = false
  }
}
</script>

<style scoped>
.model-chat-test-page {
  max-width: 1400px;
  margin: 0 auto;
  padding-top: 24px;
  padding-bottom: 32px;
}
</style>

<template>
  <v-container fluid class="model-management-page">
    <v-row class="mb-6 align-center">
      <v-col cols="12" md="7">
        <div class="d-flex flex-column gap-2">
          <div class="d-flex align-center flex-wrap gap-3">
            <h1 class="text-h4 font-weight-bold">模型管理</h1>
            <v-chip :color="canManageSources ? 'primary' : 'info'" variant="tonal" size="small">
              {{ canManageSources ? '软件管理员' : '组织管理员' }}
            </v-chip>
            <v-chip v-if="userStore.organization_name" variant="tonal" size="small" color="secondary">
              {{ userStore.organization_name }}
            </v-chip>
          </div>
          <p class="text-body-2 text-medium-emphasis">
            软件管理员负责维护模型源，组织管理员负责选择组织实际启用的模型并调整参数。
          </p>
        </div>
      </v-col>
      <v-col cols="12" md="5" class="d-flex justify-end flex-wrap gap-3">
        <v-btn
          v-if="canManageSources"
          color="primary"
          prepend-icon="mdi-plus"
          class="text-none"
          @click="showAddSourceDialog = true"
        >
          新增模型源
        </v-btn>
      </v-col>
    </v-row>

    <v-alert class="mb-6" type="info" variant="tonal" border="start">
      软件管理员可新增、删除和维护模型源；组织管理员可在已配置模型中启用模型并调整参数。
      校验连通性和获取模型列表都只针对左侧当前选中的模型源执行。
    </v-alert>

    <v-row align="stretch">
      <v-col cols="12" md="4" lg="3">
        <v-card class="source-card h-100" rounded="xl" elevation="2">
          <v-card-title class="d-flex align-center justify-space-between">
            <span class="text-h6 font-weight-bold">模型源列表</span>
            <v-btn
              v-if="canManageSources"
              icon="mdi-plus"
              size="small"
              variant="tonal"
              @click="showAddSourceDialog = true"
            />
          </v-card-title>
          <v-card-subtitle>左侧切换模型源，右侧编辑当前源及其下模型配置</v-card-subtitle>
          <v-divider></v-divider>

          <v-list class="source-list" density="comfortable">
            <v-list-item
              v-for="source in sources"
              :key="source.id"
              :active="selectedSourceId === source.id"
              class="source-item"
              @click="selectedSourceId = source.id"
            >
              <template #prepend>
                <v-avatar color="primary" variant="tonal" size="40">
                  <v-icon>mdi-brain</v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-medium">
                {{ source.name }}
              </v-list-item-title>
              <v-list-item-subtitle>{{ source.vendor }}</v-list-item-subtitle>

              <template #append>
                <div class="d-flex align-center gap-2">
                  <v-chip :color="source.status === 'active' ? 'success' : 'grey'" size="x-small" variant="tonal">
                    {{ source.status === 'active' ? '启用' : '停用' }}
                  </v-chip>
                  <v-btn
                    v-if="canManageSources"
                    icon="mdi-delete"
                    size="x-small"
                    variant="text"
                    color="error"
                    @click.stop="confirmDeleteSource(source.id)"
                  />
                </div>
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="12" md="8" lg="9">
        <v-card v-if="selectedSource" class="detail-card h-100" rounded="xl" elevation="2">
          <v-card-title class="d-flex align-start justify-space-between flex-wrap gap-3">
            <div>
              <div class="d-flex align-center gap-2 flex-wrap mb-1">
                <span class="text-h5 font-weight-bold">{{ selectedSource.name }}</span>
                <v-chip size="small" variant="tonal" color="primary">{{ selectedSource.vendor }}</v-chip>
              </div>
              <div class="text-body-2 text-medium-emphasis">{{ selectedSource.description }}</div>
            </div>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text>
            <v-row>
              <v-col cols="12" lg="7">
                <v-card variant="outlined" class="pa-4 config-block" rounded="lg">
                  <div class="d-flex align-center justify-space-between flex-wrap gap-2 mb-4">
                    <div class="text-subtitle-1 font-weight-bold">源配置</div>
                    <div class="d-flex flex-wrap gap-2">
                      <v-btn
                        v-if="canManageSources"
                        size="small"
                        color="success"
                        variant="tonal"
                        prepend-icon="mdi-check-network"
                        @click="verifySelectedSource"
                      >
                        校验当前源
                      </v-btn>
                      <v-btn
                        v-if="canManageSources"
                        size="small"
                        color="secondary"
                        variant="tonal"
                        prepend-icon="mdi-content-save"
                        @click="saveSelectedSource"
                      >
                        保存当前源
                      </v-btn>
                    </div>
                  </div>
                  <v-row dense>
                    <v-col cols="12" md="6">
                      <v-text-field v-model="selectedSource.baseUrl" label="API Base URL" variant="outlined" density="compact" hide-details :disabled="!canManageSources" />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="selectedSource.defaultModel"
                        label="校验模型（可选）"
                        hint="填写后会检查该模型是否存在；留空时只校验源连通性"
                        persistent-hint
                        variant="outlined"
                        density="compact"
                        :disabled="!canManageSources"
                      />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field v-model="selectedSource.apiKey" label="API Key" variant="outlined" density="compact" hide-details :type="showApiKey ? 'text' : 'password'" :disabled="!canManageSources" />
                    </v-col>
                    <v-col cols="12" md="6" class="d-flex align-center gap-2">
                      <v-btn :icon="showApiKey ? 'mdi-eye-off' : 'mdi-eye'" variant="tonal" @click="showApiKey = !showApiKey" />
                      <v-text-field v-model.number="selectedSource.timeout" label="超时(秒)" type="number" variant="outlined" density="compact" hide-details :disabled="!canManageSources" />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-select v-model="selectedSource.status" :items="statusOptions" label="状态" variant="outlined" density="compact" hide-details :disabled="!canManageSources" />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field v-model.number="selectedSource.retryCount" label="失败重试次数" type="number" variant="outlined" density="compact" hide-details :disabled="!canManageSources" />
                    </v-col>
                    <v-col cols="12">
                      <v-textarea v-model="selectedSource.description" label="说明" variant="outlined" rows="3" hide-details :disabled="!canManageSources" />
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>

              <v-col cols="12" lg="5">
                <v-card variant="outlined" class="pa-4 info-block" rounded="lg">
                  <div class="text-subtitle-1 font-weight-bold mb-4">源概览</div>
                  <v-list density="compact" class="py-0">
                    <v-list-item>
                      <template #prepend><v-icon color="primary">mdi-domain</v-icon></template>
                      <v-list-item-title>可见范围</v-list-item-title>
                      <v-list-item-subtitle>全局可见</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <template #prepend><v-icon color="primary">mdi-play-circle</v-icon></template>
                      <v-list-item-title>启用状态</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedSource.status === 'active' ? '已启用' : '已停用' }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <template #prepend><v-icon color="primary">mdi-update</v-icon></template>
                      <v-list-item-title>最后保存</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedSource.updatedAt }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <template #prepend><v-icon color="primary">mdi-view-list</v-icon></template>
                      <v-list-item-title>模型数量</v-list-item-title>
                      <v-list-item-subtitle>{{ selectedSource.models.length }} 个</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card>

              </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
              <div>
                <div class="text-h6 font-weight-bold">已配置模型</div>
                <div class="text-body-2 text-medium-emphasis">组织管理员可在此启用/禁用模型并配置参数，不同组织可以有不同配置。</div>
              </div>
            </div>

            <v-row>
              <v-col v-for="model in selectedSource.models" :key="model.id" cols="12" md="6">
                <v-card rounded="lg" variant="outlined" class="model-card h-100">
                  <v-card-title class="d-flex align-center justify-space-between">
                    <div>
                      <div class="text-subtitle-1 font-weight-bold">{{ model.displayName }}</div>
                      <div class="text-caption text-medium-emphasis">{{ model.modelId }}</div>
                    </div>
                    <v-switch v-model="model.enabled" color="primary" density="compact" hide-details :disabled="!canConfigureOrganizationModels" />
                  </v-card-title>
                  <v-card-text>
                    <div class="d-flex flex-wrap gap-2 mb-3">
                      <v-chip size="small" variant="tonal" color="info">{{ model.module }}</v-chip>
                      <v-chip size="small" variant="tonal" color="secondary">{{ model.useCase }}</v-chip>
                    </div>
                    <div class="text-body-2 text-medium-emphasis mb-3">{{ model.description }}</div>
                    <div class="d-flex flex-wrap gap-3 text-body-2 mb-4">
                      <span>温度 {{ model.temperature.toFixed(2) }}</span>
                      <span>Top-p {{ model.topP.toFixed(2) }}</span>
                      <span>最大输出 {{ model.maxTokens }}</span>
                    </div>
                    <div class="d-flex justify-space-between align-center">
                      <div class="text-caption text-medium-emphasis">最后更新：{{ model.updatedAt }}</div>
                      <div class="d-flex align-center gap-1">
                        <v-btn
                          size="small"
                          variant="text"
                          color="error"
                          prepend-icon="mdi-delete"
                          :disabled="!canConfigureOrganizationModels"
                          @click="removeConfiguredModel(model.id)"
                        >
                          移除
                        </v-btn>
                        <v-btn size="small" variant="text" color="primary" prepend-icon="mdi-cog" :disabled="!canConfigureOrganizationModels" @click="openModelEditor(model)">
                          配置
                        </v-btn>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <div class="d-flex align-center justify-space-between flex-wrap gap-3 mb-4">
              <div>
                <div class="text-h6 font-weight-bold">模型库</div>
                <div class="text-body-2 text-medium-emphasis">根据当前模型源获取可用模型，按行选择并添加到已配置模型。</div>
              </div>
              <v-btn
                v-if="canManageSources"
                color="info"
                variant="tonal"
                prepend-icon="mdi-download-network"
                :disabled="!selectedSource"
                @click="fetchSourceModels"
              >
                重新获取
              </v-btn>
            </div>

            <v-card variant="outlined" rounded="lg" class="model-library-list">
              <v-list density="comfortable" class="py-0">
                <v-list-item
                  v-for="candidate in selectedSource.availableModels"
                  :key="candidate.modelId"
                  class="library-item"
                >
                  <template #prepend>
                    <v-avatar color="info" variant="tonal" size="36">
                      <v-icon>mdi-database-search</v-icon>
                    </v-avatar>
                  </template>

                  <v-list-item-title class="font-weight-medium">
                    {{ candidate.displayName }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ candidate.modelId }} · {{ candidate.module }} · {{ candidate.useCase }}
                  </v-list-item-subtitle>

                  <template #append>
                    <v-btn
                      size="small"
                      color="primary"
                      variant="tonal"
                      prepend-icon="mdi-plus"
                      :disabled="!canConfigureOrganizationModels || isConfigured(candidate.modelId)"
                      @click="addModelToConfigured(candidate)"
                    >
                      {{ isConfigured(candidate.modelId) ? '已添加' : '添加' }}
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>

              <v-alert v-if="selectedSource.availableModels.length === 0" type="warning" variant="tonal" border="start" class="ma-4">
                当前还没有可选模型，请先点击“获取模型列表”。
              </v-alert>
            </v-card>
          </v-card-text>
        </v-card>

        <v-card v-else class="detail-card h-100 d-flex align-center justify-center" rounded="xl" elevation="2">
          <v-card-text class="text-center py-12">
            <v-icon size="64" color="grey-lighten-1">mdi-information-outline</v-icon>
            <div class="text-h6 mt-4">暂无可用模型源</div>
            <div class="text-body-2 text-medium-emphasis mt-2">软件管理员可以先新增一个模型源。</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showAddSourceDialog" max-width="720">
      <v-card rounded="xl">
        <v-card-title class="text-h6 font-weight-bold">新增模型源</v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col cols="12">
              <v-alert type="info" variant="tonal" border="start" density="compact">
                可先选择供应商模板自动填入参数，再按需微调。
              </v-alert>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="selectedProviderTemplate"
                :items="providerTemplateOptions"
                item-title="title"
                item-value="value"
                label="供应商模板"
                variant="outlined"
                density="compact"
                @update:modelValue="applyProviderTemplate"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newSourceForm.name"
                label="源名称"
                hint="系统内显示名称，例如 openai、deepseek"
                persistent-hint
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newSourceForm.vendor"
                label="供应商标识"
                hint="用于后端识别，例如 openai、dashscope、deepseek"
                persistent-hint
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newSourceForm.baseUrl"
                label="API Base URL"
                hint="通常形如 https://xxx/v1"
                persistent-hint
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newSourceForm.apiKey"
                label="API Key"
                variant="outlined"
                density="compact"
                type="password"
              />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="newSourceForm.description" label="描述" rows="3" variant="outlined" density="compact" />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" color="grey" @click="showAddSourceDialog = false">取消</v-btn>
          <v-btn color="primary" @click="addSource">新增</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showModelDialog" max-width="720">
      <v-card rounded="xl" v-if="editingModel">
        <v-card-title class="text-h6 font-weight-bold">模型参数配置</v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field v-model="editingModel.displayName" label="展示名称" variant="outlined" density="compact" :disabled="!canConfigureOrganizationModels" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="editingModel.modelId" label="模型ID" variant="outlined" density="compact" :disabled="!canConfigureOrganizationModels" />
            </v-col>
            <v-col cols="12" md="6">
              <v-select v-model="editingModel.module" :items="moduleOptions" label="功能模块" variant="outlined" density="compact" :disabled="!canConfigureOrganizationModels" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="editingModel.useCase" label="适用场景" variant="outlined" density="compact" :disabled="!canConfigureOrganizationModels" />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field v-model.number="editingModel.temperature" type="number" step="0.01" label="Temperature" variant="outlined" density="compact" :disabled="!canConfigureOrganizationModels" />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field v-model.number="editingModel.topP" type="number" step="0.01" label="Top-p" variant="outlined" density="compact" :disabled="!canConfigureOrganizationModels" />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field v-model.number="editingModel.maxTokens" type="number" label="最大输出" variant="outlined" density="compact" :disabled="!canConfigureOrganizationModels" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="editingModel.description" label="说明" rows="3" variant="outlined" density="compact" :disabled="!canConfigureOrganizationModels" />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" color="grey" @click="showModelDialog = false">取消</v-btn>
          <v-btn color="primary" :disabled="!canConfigureOrganizationModels" @click="saveModelConfig">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showDeleteConfirm" max-width="420">
      <v-card rounded="xl">
        <v-card-title class="text-h6 font-weight-bold">确认删除</v-card-title>
        <v-card-text>删除后该模型源及其配置将从当前页面移除，是否继续？</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" color="grey" @click="showDeleteConfirm = false">取消</v-btn>
          <v-btn color="error" @click="deleteSelectedSource">删除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import modelApi, { type ManagedModelConfig, type ModelSourceEntity, type SourceModelCandidate } from '@/api/model'
import { useSnackbarStore } from '@/stores/snackbar'
import { useUserStore } from '@/stores/user'

type ManagedModel = ManagedModelConfig
type ModelSource = ModelSourceEntity

const snackbar = useSnackbarStore()
const userStore = useUserStore()

const canManageSources = computed(() => userStore.admin_type === 'software_admin')
const canConfigureOrganizationModels = computed(() => userStore.admin_type === 'organization_admin')

const moduleOptions = ['图像真伪检测', 'LLM解释', '元数据辅助', '人工审核辅助']
const providerTemplateOptions = [
  { title: '自定义', value: 'custom' },
  { title: 'OpenAI Compatible（阿里云 DashScope）', value: 'dashscope' },
  { title: 'OpenAI 官方', value: 'openai' },
  { title: 'DeepSeek 官方', value: 'deepseek' },
  { title: 'Anthropic 官方', value: 'anthropic' },
  { title: 'Gemini OpenAI 兼容网关', value: 'gemini_openai' },
]

const providerTemplates: Record<string, { name: string; vendor: string; baseUrl: string }> = {
  dashscope: {
    name: 'openai',
    vendor: 'openai',
    baseUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  },
  openai: {
    name: 'openai',
    vendor: 'openai',
    baseUrl: 'https://api.openai.com/v1',
  },
  deepseek: {
    name: 'deepseek',
    vendor: 'deepseek',
    baseUrl: 'https://api.deepseek.com/v1',
  },
  anthropic: {
    name: 'anthropic',
    vendor: 'anthropic',
    baseUrl: 'https://api.anthropic.com/v1',
  },
  gemini_openai: {
    name: 'gemini',
    vendor: 'gemini',
    baseUrl: 'https://generativelanguage.googleapis.com/v1beta/openai/',
  },
}

const statusOptions = [
  { title: '启用', value: 'active' },
  { title: '停用', value: 'inactive' }
]
const sources = ref<ModelSource[]>([])
const selectedSourceId = ref<number | null>(sources.value[0]?.id ?? null)
const showApiKey = ref(false)
const showAddSourceDialog = ref(false)
const showModelDialog = ref(false)
const showDeleteConfirm = ref(false)
const deletingSourceId = ref<number | null>(null)
const editingModel = ref<ManagedModel | null>(null)
const selectedProviderTemplate = ref('custom')

const newSourceForm = ref({
  name: '',
  vendor: '',
  baseUrl: '',
  apiKey: '',
  description: ''
})

const selectedSource = computed(() => sources.value.find((source) => source.id === selectedSourceId.value) ?? null)

function resolveErrorMessage(error: unknown, fallback: string) {
  const maybeError = error as {
    response?: {
      data?: {
        error?: string
        message?: string
      }
    }
  }

  return maybeError.response?.data?.error || maybeError.response?.data?.message || fallback
}

watch(selectedSourceId, () => {
  showApiKey.value = false
})

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

    if (!sources.value.length) {
      selectedSourceId.value = null
      return
    }

    const hasSelected = sources.value.some((source) => source.id === selectedSourceId.value)
    if (!hasSelected) {
      selectedSourceId.value = sources.value[0].id
    }
  } catch (error) {
    snackbar.showMessage('加载模型源失败', 'error')
  }
}

async function fetchSourceModels() {
  if (!selectedSource.value) {
    snackbar.showMessage('请先在左侧选择一个模型源', 'warning')
    return
  }
  if (!canManageSources.value) {
    snackbar.showMessage('只有软件管理员可以获取模型列表', 'warning')
    return
  }

  if (!selectedSource.value.baseUrl || !selectedSource.value.apiKey) {
    snackbar.showMessage('请先填写当前模型源的 base URL 与 API Key', 'warning')
    return
  }

  try {
    const response = await modelApi.fetchSourceModels(selectedSource.value.id, {
      base_url: selectedSource.value.baseUrl,
      api_key: selectedSource.value.apiKey,
      timeout: selectedSource.value.timeout,
    })
    selectedSource.value.availableModels = response.data.availableModels || []
    snackbar.showMessage(`模型源 ${selectedSource.value.name} 已获取 ${selectedSource.value.availableModels.length} 个模型`, 'success')
  } catch (error) {
    snackbar.showMessage(resolveErrorMessage(error, '获取模型列表失败'), 'error')
  }
}

function applyProviderTemplate(templateKey: string | null) {
  if (!templateKey || templateKey === 'custom') return

  const template = providerTemplates[templateKey]
  if (!template) return

  newSourceForm.value.vendor = template.vendor
  newSourceForm.value.baseUrl = template.baseUrl
  if (!newSourceForm.value.name.trim()) {
    newSourceForm.value.name = template.name
  }
}

function isConfigured(modelId: string) {
  return !!selectedSource.value?.models.some((model) => model.modelId === modelId)
}

async function addModelToConfigured(candidate: SourceModelCandidate) {
  if (!selectedSource.value) return
  if (!canConfigureOrganizationModels.value) {
    snackbar.showMessage('只有组织管理员可以配置组织模型', 'warning')
    return
  }

  if (isConfigured(candidate.modelId)) {
    snackbar.showMessage('该模型已在已配置模型中', 'info')
    return
  }

  try {
    const response = await modelApi.addOrganizationModelConfig(selectedSource.value.id, {
      provider_model_id: candidate.id,
      model_id: candidate.modelId,
      enabled: true,
      temperature: 0.2,
      top_p: 0.9,
      max_tokens: 2048,
      description: candidate.description,
    })
    selectedSource.value.models.push(response.data.config)
    snackbar.showMessage('模型已添加到已配置模型', 'success')
  } catch (error) {
    snackbar.showMessage('添加模型配置失败', 'error')
  }
}

async function removeConfiguredModel(modelId: number) {
  if (!selectedSource.value) return
  if (!canConfigureOrganizationModels.value) {
    snackbar.showMessage('只有组织管理员可以调整组织模型', 'warning')
    return
  }

  try {
    await modelApi.deleteOrganizationModelConfig(modelId)
    selectedSource.value.models = selectedSource.value.models.filter((model) => model.id !== modelId)
    snackbar.showMessage('模型已从已配置模型移除', 'success')
  } catch (error) {
    snackbar.showMessage('移除模型配置失败', 'error')
  }
}

async function saveSelectedSource() {
  if (!selectedSource.value) return
  if (!canManageSources.value) {
    snackbar.showMessage('只有软件管理员可以保存模型源配置', 'warning')
    return
  }

  try {
    await modelApi.updateAIModel(selectedSource.value.id, {
      name: selectedSource.value.name,
      vendor: selectedSource.value.vendor,
      base_url: selectedSource.value.baseUrl,
      api_key: selectedSource.value.apiKey,
      default_model: selectedSource.value.defaultModel,
      timeout: selectedSource.value.timeout,
      retry_count: selectedSource.value.retryCount,
      status: selectedSource.value.status,
      description: selectedSource.value.description,
    })
    snackbar.showMessage('模型源配置已保存', 'success')
  } catch (error) {
    snackbar.showMessage('保存模型源配置失败', 'error')
  }
}

async function verifySelectedSource() {
  if (!selectedSource.value) return
  if (!canManageSources.value) {
    snackbar.showMessage('只有软件管理员可以校验模型源', 'warning')
    return
  }

  try {
    const response = await modelApi.verifyAIModelConfig({
      base_url: selectedSource.value.baseUrl,
      api_key: selectedSource.value.apiKey,
      model_name: selectedSource.value.defaultModel,
    })
    if (response.data.model_exists) {
      snackbar.showMessage(`连接正常：${selectedSource.value.name}`, 'success')
    } else {
      snackbar.showMessage(response.data.message || '连接成功但默认模型不存在', 'warning')
    }
  } catch (error) {
    snackbar.showMessage(resolveErrorMessage(error, '模型源校验失败'), 'error')
  }
}

async function addSource() {
  if (!canManageSources.value) {
    snackbar.showMessage('只有软件管理员可以新增模型源', 'warning')
    return
  }

  if (!newSourceForm.value.name || !newSourceForm.value.vendor || !newSourceForm.value.baseUrl || !newSourceForm.value.apiKey) {
    snackbar.showMessage('请完整填写模型源信息', 'warning')
    return
  }

  try {
    const response = await modelApi.addAIModel({
      name: newSourceForm.value.name,
      vendor: newSourceForm.value.vendor,
      base_url: newSourceForm.value.baseUrl,
      api_key: newSourceForm.value.apiKey,
      timeout: 30,
      retry_count: 2,
      status: 'active',
      description: newSourceForm.value.description,
    })

    const source = response.data?.source as ModelSource | undefined
    if (source) {
      sources.value.unshift(source)
      selectedSourceId.value = source.id
    } else {
      await loadSources()
    }

    showAddSourceDialog.value = false
    selectedProviderTemplate.value = 'custom'
    newSourceForm.value = {
      name: '',
      vendor: '',
      baseUrl: '',
      apiKey: '',
      description: ''
    }
    snackbar.showMessage('模型源新增成功', 'success')
  } catch (error) {
    snackbar.showMessage('模型源新增失败', 'error')
  }
}

function confirmDeleteSource(sourceId: number) {
  deletingSourceId.value = sourceId
  showDeleteConfirm.value = true
}

async function deleteSelectedSource() {
  if (!canManageSources.value || deletingSourceId.value === null) {
    showDeleteConfirm.value = false
    return
  }

  try {
    await modelApi.deleteAIModel(deletingSourceId.value)
    sources.value = sources.value.filter((source) => source.id !== deletingSourceId.value)
    if (selectedSourceId.value === deletingSourceId.value) {
      selectedSourceId.value = sources.value[0]?.id ?? null
    }
    deletingSourceId.value = null
    showDeleteConfirm.value = false
    snackbar.showMessage('模型源已删除', 'success')
  } catch (error) {
    snackbar.showMessage('删除模型源失败', 'error')
  }
}

function openModelEditor(model: ManagedModel | undefined) {
  if (!model) return
  if (!canConfigureOrganizationModels.value) {
    snackbar.showMessage('只有组织管理员可以配置组织模型', 'warning')
    return
  }
  editingModel.value = JSON.parse(JSON.stringify(model)) as ManagedModel
  showModelDialog.value = true
}

async function saveModelConfig() {
  if (!selectedSource.value || !editingModel.value) return
  if (!canConfigureOrganizationModels.value) {
    snackbar.showMessage('只有组织管理员可以配置组织模型', 'warning')
    return
  }

  try {
    const response = await modelApi.updateOrganizationModelConfig(editingModel.value.id, {
      enabled: editingModel.value.enabled,
      temperature: editingModel.value.temperature,
      top_p: editingModel.value.topP,
      max_tokens: editingModel.value.maxTokens,
      description: editingModel.value.description,
    })

    const index = selectedSource.value.models.findIndex((model) => model.id === editingModel.value?.id)
    if (index >= 0) {
      selectedSource.value.models[index] = response.data.config
    }

    showModelDialog.value = false
    snackbar.showMessage('模型配置已更新', 'success')
  } catch (error) {
    snackbar.showMessage('更新模型配置失败', 'error')
  }
}
</script>

<style scoped>
.model-management-page {
  max-width: 1600px;
  margin: 0 auto;
  padding-top: 24px;
  padding-bottom: 32px;
}

.source-card,
.detail-card {
  background:
    radial-gradient(circle at top right, rgba(25, 118, 210, 0.08), transparent 30%),
    linear-gradient(180deg, rgba(var(--v-theme-surface), 1) 0%, rgba(var(--v-theme-surface), 0.96) 100%);
}

.source-list {
  max-height: calc(100vh - 260px);
  overflow-y: auto;
}

.source-item {
  margin: 6px 12px;
  border-radius: 16px;
  transition: transform 0.18s ease, background-color 0.18s ease;
}

.source-item:hover {
  transform: translateY(-1px);
}

.config-block,
.info-block,
.model-card {
  background: rgb(var(--v-theme-surface));
}

.model-card {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.model-library-list {
  background: rgb(var(--v-theme-surface));
}

.library-item {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.4);
}

.library-item:last-child {
  border-bottom: none;
}

@media (max-width: 960px) {
  .model-management-page {
    padding-top: 12px;
  }
}
</style>
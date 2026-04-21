import http from './request'

export interface VerifyModelConfigPayload {
  base_url: string
  api_key: string
  model_name: string
  organization_id?: number | null
}

export interface SourceModelCandidate {
  id: number
  modelId: string
  displayName: string
  module: string
  useCase: string
  description: string
}

export interface ManagedModelConfig {
  id: number
  providerModelId: number
  modelId: string
  displayName: string
  module: string
  useCase: string
  enabled: boolean
  temperature: number
  topP: number
  maxTokens: number
  description: string
  updatedAt: string
}

export interface ModelSourceEntity {
  id: number
  name: string
  vendor: string
  scope: 'global'
  status: 'active' | 'inactive'
  baseUrl: string
  apiKey: string
  defaultModel: string
  timeout: number
  retryCount: number
  description: string
  updatedAt: string
  availableModels: SourceModelCandidate[]
  models: ManagedModelConfig[]
}

export interface ListAIModelsResponse {
  admin_type: 'software_admin' | 'organization_admin'
  sources: ModelSourceEntity[]
}

export interface CreateModelSourcePayload {
  name: string
  vendor: string
  scope?: 'global'
  base_url: string
  api_key: string
  default_model?: string
  timeout?: number
  retry_count?: number
  status?: 'active' | 'inactive'
  description?: string
}

export interface UpdateModelSourcePayload {
  name?: string
  vendor?: string
  scope?: 'global'
  base_url?: string
  api_key?: string
  default_model?: string
  timeout?: number
  retry_count?: number
  status?: 'active' | 'inactive'
  description?: string
}

export interface AddOrganizationModelConfigPayload {
  provider_model_id?: number
  model_id?: string
  enabled?: boolean
  temperature?: number
  top_p?: number
  max_tokens?: number
  description?: string
}

export interface FetchSourceModelsPayload {
  base_url?: string
  api_key?: string
  timeout?: number
}

export interface UpdateOrganizationModelConfigPayload {
  enabled?: boolean
  temperature?: number
  top_p?: number
  max_tokens?: number
  description?: string
}

export default {
  listAIModels() {
    return http.get<ListAIModelsResponse>('/admin/models/')
  },

  verifyAIModelConfig(data: VerifyModelConfigPayload) {
    return http.post('/admin/models/verify/', data)
  },

  addAIModel(data: CreateModelSourcePayload) {
    return http.post('/admin/models/add/', data)
  },

  updateAIModel(modelId: number, data: UpdateModelSourcePayload) {
    return http.put(`/admin/models/${modelId}/update/`, data)
  },

  deleteAIModel(modelId: number) {
    return http.delete(`/admin/models/${modelId}/delete/`)
  },

  fetchSourceModels(sourceId: number, data?: FetchSourceModelsPayload) {
    return http.post<{ availableModels: SourceModelCandidate[] }>(`/admin/models/${sourceId}/fetch-models/`, data)
  },

  addOrganizationModelConfig(sourceId: number, data: AddOrganizationModelConfigPayload) {
    return http.post<{ config: ManagedModelConfig }>(`/admin/models/${sourceId}/configs/add/`, data)
  },

  updateOrganizationModelConfig(configId: number, data: UpdateOrganizationModelConfigPayload) {
    return http.put<{ config: ManagedModelConfig }>(`/admin/models/configs/${configId}/update/`, data)
  },

  deleteOrganizationModelConfig(configId: number) {
    return http.delete(`/admin/models/configs/${configId}/delete/`)
  }
}
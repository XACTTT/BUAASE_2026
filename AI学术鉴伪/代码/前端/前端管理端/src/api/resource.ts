import http from './request'

export interface Resource {
  id: number
  type: 'paper' | 'review' | 'image' | 'comprehensive'
  file_name: string
  file_format: string
  upload_time: string
  uploader_id: number
  uploader_name: string
  uploader_email: string
  classification: string
  detection_time: string | null
  detection_result: string | null
  detection_status: 'pending' | 'detecting' | 'completed' | 'failed'
  task_id: number | null
  related_resources: RelatedResource[]
  // 新增字段
  title?: string
  author?: string
  organization?: string
  subject?: string
  // 检测类型
  detection_type: '图像' | '论文' | 'review' | '综合' | '未检测'
}

export interface RelatedResource {
  id: number
  type: string
  file_name: string
  relation_type: string
}

export interface ResourceListParams {
  page: number
  page_size: number
  type?: string
  query?: string
  user_id?: number
  classification?: string
  start_time?: string
  end_time?: string
  detection_result?: string
}

export interface ResourceListResponse {
  total_count: number
  page: number
  total_pages: number
  resources: Resource[]
}

// 结构化检测结果
export interface StructuredResult {
  task_id: number
  task_type: 'image' | 'paper_text' | 'review_text' | 'multi_material'
  status: string
  overall_is_fake?: boolean
  confidence_score?: number
  result?: {
    dimensions?: { name: string; score: number; summary?: string }[]
    evidence?: any
    llm_analysis?: any
    fake_images?: { result_id: string; image_url: string; image_id: string }[]
    normal_images?: { result_id: string; image_url: string; image_id: string }[]
  }
  ai_response?: any
  detection_time?: string
}

export default {
  // 获取学术资源列表
  getResources(params: ResourceListParams) {
    return http.get<ResourceListResponse>('/admin/resources/', { params })
  },

  // 获取资源详情
  getResourceDetail(resourceId: number) {
    return http.get<Resource>(`/admin/resources/${resourceId}/`)
  },

  // 更新资源分类与元数据
  updateResourceMetadata(resourceId: number, data: {
    classification?: string
    tags?: string[]
    is_public?: boolean
  }) {
    return http.put(`/admin/resources/${resourceId}/`, data)
  },

  // 删除学术资源
  deleteResource(resourceId: number) {
    return http.delete(`/admin/resources/${resourceId}/`)
  },

  // 终止检测任务
  terminateDetection(taskId: number) {
    return http.post(`/admin/detection-task/${taskId}/terminate/`)
  },

  // 删除检测任务
  deleteDetection(taskId: number) {
    return http.delete(`/admin/detection-task/${taskId}/`)
  },

  // 获取结构化检测结果
  getDetectionResult(taskId: number) {
    return http.get<StructuredResult>(`/tasks/${taskId}/structured-result/`)
  },

  // 获取资源预览
  previewResource(resourceId: number, resourceType: string = 'file') {
    return http.get<Blob>(`/preview/${resourceType}/${resourceId}/`, { responseType: 'blob' })
  },

  // ========== 检测结果详情 API（从用户端迁移） ==========

  // 获取疑似造假图片列表
  getFakeImages(taskId: number | string) {
    return http.get(`/tasks/${taskId}/fake_results/`, { params: { include_image: 1 } })
  },

  // 获取正常图片列表
  getNormalImages(taskId: number | string) {
    return http.get(`/tasks/${taskId}/normal_results/`, { params: { include_image: 1 } })
  },

  // 获取单张图片检测结果详情
  getSingleImageResult(resultId: string | number) {
    return http.get(`/results/${resultId}/`)
  },

  // 获取任务级LLM分析
  getTaskLlmAnalysis(taskId: number | string) {
    return http.get(`/tasks/${taskId}/llm-analysis/`)
  },

  // 获取任务文本检测结果列表
  getTaskTextResults(taskId: number | string) {
    return http.get(`/tasks/${taskId}/text_results/`)
  },

  // 获取单条文本检测结果
  getSingleTextResult(resourceId: number | string) {
    return http.get(`/detection/text/${resourceId}/`)
  },

  // 通过image_id获取检测结果
  getImageDetectionByImageId(imageId: number | string) {
    return http.get(`/results_image/${imageId}/`)
  },

  // 下载检测报告
  downloadReport(taskId: number | string) {
    return http.get(`/tasks/${taskId}/report/`, { responseType: 'blob' })
  },
}
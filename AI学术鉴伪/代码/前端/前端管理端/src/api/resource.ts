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
  related_resources?: RelatedResource[]
  // 新增字段
  title?: string
  author?: string
  organization?: string
  editor?: string
  subject?: string
  status?: string
  review_count?: number
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
  }
}
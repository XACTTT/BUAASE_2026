import http from './request'

const LONG_REQUEST_TIMEOUT = 120000
const MEDIUM_REQUEST_TIMEOUT = 60000

export default {
  //发布审核任务
  dispatchAnnual(data: any) {
    return http.post('/create_review_task_with_admin_check/', data, { timeout: 30000 })
  },

  //data是taskId
  //返回某个task的所有人工审核任务的完成情况，只返回百分比
  getAllAnnual(data: any) {
    return http.get(`/get_task_completion_status/${data}`)
  },

  //返回某个task的所有images和所有人工审核的结果
  getAnnualDetail(data: any) {
    return http.get(`/get_task_detail/${data}/`, { timeout: LONG_REQUEST_TIMEOUT })
  },

  //返回特定审核员对特定任务的审核结果
  getReviewerDetail(data: any) {
    return http.get(`/get_task_reviewer_detail/${data.taskId}/${data.reviewer_id}`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  getAllReviewers() {
    return http.get('/get_all_reviewers/')
  },

  getReviewers(data: any) {
    return http.get(`publishers/${data.publisher_id}/reviewers/`)
  },

  //获取某个出版社所有检测的任务
  getAllDetectionTask(data: any) {
    return http.get('/user-tasks/', { params: data })
  },

  //提交AI检测任务
  submitDetection(data: any) {
    return http.post('/detection/submit/', data, { timeout: LONG_REQUEST_TIMEOUT })
  },

  getStructuredTaskResult(data: any, config: any = {}) {
    return http.get(`/tasks/${data}/structured-result/`, {
      timeout: LONG_REQUEST_TIMEOUT,
      ...config,
    })
  },

  //提交AI文本检测任务
  submitTextDetection(data: any) {
    return http.post('/detection/submit_text/', data, { timeout: LONG_REQUEST_TIMEOUT })
  },

  //获取某个任务的所有文本的AI检测结果
  getTaskTextResults(data: any) {
    return http.get(`/tasks/${data}/text_results/`, { timeout: LONG_REQUEST_TIMEOUT })
  },

  //获取单条文本记录的AI检测结果详情
  getSingleTextResult(data: any) {
    return http.get(`/detection/text/${data}/`, { timeout: LONG_REQUEST_TIMEOUT })
  },

  getFakeImage(data: any) {
    return http.get(`/tasks/${data.task_id}/fake_results/?include_image=${data.include_image}`, { timeout: LONG_REQUEST_TIMEOUT })
  },

  getNormalImage(data: any) {
    return http.get(`/tasks/${data.task_id}/normal_results/?include_image=${data.include_image}`, { timeout: LONG_REQUEST_TIMEOUT })
  },

  getSingleImageResult(data: any) {
    return http.get(`/results/${data}/`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  getImageDetectionByImageId(imageId: number) {
    return http.get(`/results_image/${imageId}/`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  getTaskLlmAnalysis(data: any) {
    return http.get(`/tasks/${data}/llm-analysis/`, { timeout: LONG_REQUEST_TIMEOUT })
  },

  downloadReport(data: any) {
    return http.get(`/tasks/${data}/report/`, {
      responseType: 'blob',
      timeout: LONG_REQUEST_TIMEOUT,
    })
  },

  downloadReviewReport(data: any) {
    const manualReviewId = data.manual_review_id ?? data.review_id ?? data.review_request_id
    return http.get(`/manual-review/${manualReviewId}/report/`, {
      responseType: 'blob',
      timeout: LONG_REQUEST_TIMEOUT,
    })
  },

  getPublisherReviewTasks(params: {
    page?: number
    page_size?: number
    status?: string
    startTime?: string
    endTime?: string
  }) {
    return http.get('/get_publisher_review_tasks/', { params })
  },

  getTaskSummary() {
    return http.get('/task-summary/')
  },

  ifHasPermission(params: {
    task_id: string
  }) {
    return http.get(`/publisher-dectectiontask-access/`, { params })
  },

  //publisher端返回人工审核表头
  getRequestDetail(data: any) {
    return http.get(`/get_request_detail/${data.review_request_id}/`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  getManualReviewsByRequest(data: any) {
    return http.get(`/manual-review/${data.review_request_id}/`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  //publisher获取单个图片的所有人工审核结果
  getImageReviewAll(data: any) {
    return http.get(`/get_img_review_all/?review_request_id=${data.review_request_id}&img_id=${data.img_id}`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  //publisher获得单张图片的单个人的详细人工审核结果
  getImageReviewDetail(data: any) {
    return http.get(`/get_image_review/?review_request_id=${data.review_request_id}&img_id=${data.img_id}&reviewer_id=${data.reviewer_id}`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  //publisher根据imgid获取detectionid
  getTextReviewAll(data: any) {
    return http.get('/get_text_review_all/', {
      params: { review_request_id: data.review_request_id, text_id: data.text_id },
      timeout: MEDIUM_REQUEST_TIMEOUT,
    })
  },

  getTextReviewDetail(data: any) {
    return http.get('/get_text_review/', {
      params: { review_request_id: data.review_request_id, text_id: data.text_id, reviewer_id: data.reviewer_id },
      timeout: MEDIUM_REQUEST_TIMEOUT,
    })
  },

  getDetectionID(data: any) {
    return http.get(`/tasks_image/${data.img_id}/getdr/`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  deleteDetectionTask(data: any) {
    return http.delete(`/detection-task-delete/${data.task_id}/`)
  },

  getDetectionMethods() {
    return http.get('/detection/methods/')
  },

  getResourceContainers() {
    return http.get('/resource-containers/')
  },

  createResourceContainer(data: { container_type: string; title: string; metadata?: Record<string, any> }) {
    return http.post('/resource-containers/', data)
  }

}

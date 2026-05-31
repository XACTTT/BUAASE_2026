import http from './request'

export default {
  submitReview(manual_review_id: number, data: any) {
    return http.post(`/post_review/${manual_review_id}/`, data)
  },
  getReviewerTasks(params: any) {
    return http.get('/get_reviewer_tasks/', { params })
  },
  getReviewRequest(params: any) {
    return http.get('/get_publisher_review_tasks/', { params })
  },

  /** Legacy endpoint (admin) - returns imgs/texts with embedded ai_detection per text */
  getReviewTaskDetail(data: any) {
    return http.get(`/get_review_request_detail/${data.manual_review_id}/`, { timeout: 30000 })
  },

  /** New endpoint - returns task_type, review_config, structured_result, image/text reviews */
  getReviewDetail(data: any) {
    return http.get(`/get_review_detail/${data.manual_review_id}/`, { timeout: 30000 })
  },

  /** Get review config for a specific task type */
  getReviewIndicators(params: any) {
    return http.get('/get_review_indicators/', { params })
  },

  getMaskImage(data: any) {
    return http.get(`/results_image/${data.img_id}/`)
  },

  getTaskCount() {
    return http.get('/reviewer/tasks/')
  },

  getRecentActivities() {
    return http.get('/reviewer/activity_logs/')
  },

  getDetectionResult(data: any) {
    return http.get(`/tasks_image/${data.img_id}/report/`)
  }

}

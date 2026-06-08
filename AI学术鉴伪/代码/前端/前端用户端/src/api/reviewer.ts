import http from './request'

const LONG_REQUEST_TIMEOUT = 120000
const MEDIUM_REQUEST_TIMEOUT = 60000

export default {
  submitReview(manual_review_id: number, data: any) {
    return http.post(`/post_review/${manual_review_id}/`, data, { timeout: LONG_REQUEST_TIMEOUT })
  },
  getReviewerTasks(params: any) {
    return http.get('/get_reviewer_tasks/', { params })
  },
  getReviewRequest(params: any) {
    return http.get('/get_publisher_review_tasks/', { params })
  },

  /** Legacy endpoint (admin) - returns imgs/texts with embedded ai_detection per text */
  getReviewTaskDetail(data: any) {
    return http.get(`/get_review_request_detail/${data.manual_review_id}/`, { timeout: LONG_REQUEST_TIMEOUT })
  },

  /** New endpoint - returns task_type, review_config, structured_result, image/text reviews */
  getReviewDetail(data: any) {
    return http.get(`/get_review_detail/${data.manual_review_id}/`, { timeout: LONG_REQUEST_TIMEOUT })
  },

  /** Get review config for a specific task type */
  getReviewIndicators(params: any) {
    return http.get('/get_review_indicators/', { params })
  },

  getMaskImage(data: any) {
    return http.get(`/results_image/${data.img_id}/`, { timeout: MEDIUM_REQUEST_TIMEOUT })
  },

  getTaskCount() {
    return http.get('/reviewer/tasks/')
  },

  getRecentActivities() {
    return http.get('/reviewer/activity_logs/')
  },

  getDetectionResult(data: any) {
    return http.get(`/tasks_image/${data.img_id}/report/`, { timeout: LONG_REQUEST_TIMEOUT })
  }

}

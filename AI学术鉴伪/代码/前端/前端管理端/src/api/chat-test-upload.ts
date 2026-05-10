import http from './request'

export default {
  uploadTestFiles(data: FormData) {
    return http.post('/admin/models/chat-upload/', data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}

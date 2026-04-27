import http from './request'

export default {
  uploadFile(data: any) {
    return http.post('/upload/', data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  getExtractedImages(data: any) {
    const batchQuery = data.batch_id ? `&batch_id=${encodeURIComponent(data.batch_id)}` : ''
    return http.get(`/upload/${data.file_id}/extract_images/?page=${data.page_number}&page_size=${data.page_size}${batchQuery}`)
  },

  getExtractedContents(data: any) {
    return http.get(`/upload/${data.file_id}/extract_contents/?content_type=${data.content_type}&page=${data.page_number}&page_size=${data.page_size}`)
  },

  addTag(data: any) {
    console.log(data)
    return http.post(`/upload/${data.fileId}/addTag/`, {tag:data.tag})
  }
}

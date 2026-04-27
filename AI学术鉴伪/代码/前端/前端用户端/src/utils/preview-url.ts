export const resolveApiAssetUrl = (path: string): string => {
  if (!path) {
    return ''
  }

  if (/^https?:\/\//i.test(path)) {
    return path
  }

  const envBase = String(import.meta.env.VITE_API_URL || '').trim()
  if (!envBase) {
    return path
  }

  const normalizedBase = envBase.replace(/\/api\/?$/i, '')
  if (path.startsWith('/')) {
    return `${normalizedBase}${path}`
  }
  return `${normalizedBase}/${path}`
}

export const appendPreviewToken = (url: string): string => {
  if (!url || !url.includes('/api/preview/')) {
    return url
  }

  const token = localStorage.getItem('2-token')
  if (!token) {
    return url
  }

  const separator = url.includes('?') ? '&' : '?'
  return `${url}${separator}token=${encodeURIComponent(token)}`
}

export const buildOriginalDownloadUrl = (url: string): string => {
  if (!url) {
    return ''
  }
  const sep = url.includes('?') ? '&' : '?'
  return `${url}${sep}download=1`
}

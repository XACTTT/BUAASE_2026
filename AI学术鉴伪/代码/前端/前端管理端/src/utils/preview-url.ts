/**
 * Resolve a relative or absolute API asset path to a full URL.
 * Adapted from user frontend for admin frontend (uses 1-token instead of 2-token).
 */
export const resolveApiAssetUrl = (path: string): string => {
  if (!path) {
    return ''
  }

  const envBase = String(import.meta.env.VITE_API_URL || '').trim()
  const backendHosts = ['http://116.63.14.7']
  if (envBase) {
    try {
      const url = new URL(envBase)
      backendHosts.push(`${url.protocol}//${url.host}`)
    } catch { /* ignore */ }
  }

  for (const host of backendHosts) {
    if (path.startsWith(host)) {
      return path.slice(host.length) || '/'
    }
  }

  if (/^https?:\/\//i.test(path)) {
    return path
  }

  if (!envBase) {
    return path
  }

  const normalizedBase = envBase.replace(/\/api\/?$/i, '')
  if (path.startsWith('/')) {
    return `${normalizedBase}${path}`
  }
  return `${normalizedBase}/${path}`
}

export const resolveImageUrl = (url: string): string => {
  const resolved = resolveApiAssetUrl(url)
  return appendPreviewToken(resolved)
}

export const appendPreviewToken = (url: string): string => {
  if (!url || !url.includes('/api/preview/')) {
    return url
  }

  const token = localStorage.getItem('1-token')
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

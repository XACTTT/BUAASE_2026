/**
 * Resolve a relative or absolute API asset path to a full URL.
 *
 * Handles:
 *  - already-absolute URLs (http/https) -> return as-is
 *  - relative paths starting with "/"    -> prepend VITE_API_URL (without trailing /api)
 *  - relative paths without leading "/"  -> prepend VITE_API_URL + "/"
 *  - missing VITE_API_URL               -> return path unchanged (dev proxy handles it)
 */
export const resolveApiAssetUrl = (path: string): string => {
  if (!path) {
    return ''
  }

  // For absolute URLs pointing to the backend, strip the host to use the dev proxy
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

/**
 * Resolve an image URL and optionally append a JWT preview token.
 *
 * This is the single entry point all components should use for displaying
 * images returned by the backend. It handles every URL pattern the API may
 * return:
 *   - Full absolute URLs with host
 *   - Relative paths like /api/preview/image/123/
 *   - Paths without leading slash
 *
 * If the resolved URL points to the /api/preview/ endpoint, the stored JWT
 * token is appended automatically so the image can be fetched.
 */
export const resolveImageUrl = (url: string): string => {
  const resolved = resolveApiAssetUrl(url)
  return appendPreviewToken(resolved)
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

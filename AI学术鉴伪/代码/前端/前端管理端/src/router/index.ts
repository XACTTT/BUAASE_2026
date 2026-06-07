/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'
import { isLoggedIn } from '@/api/user'
import { useUserStore } from '@/stores/user'

type RouteLike = { path: string; fullPath: string }
type NavigationGuardNext = (location?: string | false | void) => void

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: setupLayouts(routes),
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err: Error, to: RouteLike) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

const fallbackForAdminType = (adminType: string) => {
  if (adminType === 'software_admin') return '/organizations'
  if (adminType === 'organization_admin') return '/organization_profile'
  return '/'
}

const requiredAdminTypeForPath = (path: string) => {
  if (path === '/organizations') return 'software_admin'
  if (path === '/organization_profile') return 'organization_admin'
  return ''
}

router.beforeEach(async (to: RouteLike, _from: RouteLike, next: NavigationGuardNext) => {
  const hasToken = !!localStorage.getItem('1-token')
  const isAuthenticated = isLoggedIn.value && hasToken

  if (!isAuthenticated) {
    isLoggedIn.value = false
    localStorage.setItem('1-isLoggedIn', 'false')

    if (to.path === '/login') {
      next()
    } else {
      next('/login')
    }
  } else {
    if (to.path === '/login') {
      next('/')
      return
    }

    const userStore = useUserStore()
    if (!userStore.hasUserInfo) {
      const loaded = await userStore.fetchUserInfo()
      if (!loaded) {
        isLoggedIn.value = false
        localStorage.setItem('1-isLoggedIn', 'false')
        localStorage.removeItem('1-token')
        localStorage.removeItem('1-refresh')
        next('/login')
        return
      }
    }

    const requiredAdminType = requiredAdminTypeForPath(to.path)
    if (requiredAdminType && userStore.admin_type !== requiredAdminType) {
      next(fallbackForAdminType(userStore.admin_type))
      return
    }

    next()
  }
})
export default router

// stores/user.ts
import { defineStore } from 'pinia';
import user from '@/api/user';

interface UserState {
  username: string;
  email: string;
  role: string;
  profile: string;
  avatar: string;
  isLoaded: boolean;
  id: number;
  organization_name: string;
  organization: number
  permission: number | null
}

const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

const normalizePermission = (permission: number | string | null | undefined): number | null => {
  if (permission === null || permission === undefined) return null

  const parsed = typeof permission === 'number' ? permission : Number.parseInt(String(permission), 10)
  if (!Number.isFinite(parsed)) return null

  const permissionString = String(parsed)
  const isOldPermissionFormat =
    parsed > 127 ||
    (parsed > 0 && permissionString.length <= 4 && [...permissionString].every(char => char === '0' || char === '1'))

  if (!isOldPermissionFormat) {
    return parsed
  }

  const oldPermission = permissionString.padStart(4, '0')
  let result = 0
  if (oldPermission[0] === '1') result |= 64 | 32 | 16 | 8
  if (oldPermission[1] === '1') result |= 4
  if (oldPermission[2] === '1') result |= 2
  if (oldPermission[3] === '1') result |= 1
  return result
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    username: '',
    email: '',
    role: '',
    profile: '',
    avatar: './192.png',
    isLoaded: false,
    id: 0,
    organization: 0,
    permission: null,
    organization_name: ''
  }),

  actions: {
    async fetchUserInfo() {
      try {
        const response = await user.getUserInfo();
        this.username = response.data.username || '';
        this.email = response.data.email || '';
        this.role = response.data.role || '';
        this.profile = response.data.profile || '';
        this.avatar = response.data.avatar ? `${API_BASE_URL}${response.data.avatar}` : './192.png';
        this.isLoaded = true;
        this.id = response.data.id;
        this.organization = response.data.organization
        this.organization_name = response.data.organization_name
        this.permission = normalizePermission(response.data.permission)
        return true;
      } catch (error) {
        console.error('获取用户信息失败:', error);
        this.isLoaded = false;
        return false;
      }
    },

    async updateAvatar(file: File) {
      try {
        const formData = new FormData();
        formData.append('avatar', file);

        const response = await user.updateUserAvatar(formData);
        if (response.data.avatar) {
          this.avatar = `${API_BASE_URL}${response.data.avatar}`;
          this.fetchUserInfo();
        }
        return true;
      } catch (error) {
        console.error('更新头像失败:', error);
        return false;
      }
    },

    clearUserInfo() {
      this.username = '';
      this.email = '';
      this.role = '';
      this.profile = '';
      this.avatar = './192.png';
      this.isLoaded = false;
      this.id = 0;
      this.organization = 0;
      this.organization_name = ''
      this.permission = null
    }
  },

  getters: {
    displayName: (state) => state.username || '未登录',
    userRole: (state) => state.role || '未设置',
    hasUserInfo: (state) => state.isLoaded
  }
}); 

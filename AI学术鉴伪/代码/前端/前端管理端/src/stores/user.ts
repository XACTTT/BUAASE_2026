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
  admin_type: string;
  organization: number;
  organization_name: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL;
const DEFAULT_AVATAR = '/default-avatar.svg';

function resolveAvatarUrl(avatar?: string | null): string {
  if (!avatar) {
    return DEFAULT_AVATAR;
  }
  if (avatar.startsWith('http://') || avatar.startsWith('https://')) {
    return avatar;
  }
  return `${API_BASE_URL}${avatar}`;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    username: '',
    email: '',
    role: '',
    profile: '',
    avatar: DEFAULT_AVATAR,
    isLoaded: false,
    admin_type: '',
    organization: 0,
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
        this.avatar = resolveAvatarUrl(response.data.avatar);
        this.admin_type = response.data.admin_type;
        this.isLoaded = true;
        this.organization = response.data.organization;
        this.organization_name = response.data.organization_name || '';
        return true;
      } catch (error) {
        console.error('获取用户信息失败:', error);
        this.isLoaded = false;
        return false;
      }
    },

    clearUserInfo() {
      this.username = '';
      this.email = '';
      this.role = '';
      this.profile = '';
      this.avatar = DEFAULT_AVATAR;
      this.isLoaded = false;
      this.admin_type = '';
      this.organization = 0;
      this.organization_name = '';
    }
  },

  getters: {
    displayName: (state) => state.username || '未登录',
    userRole: (state) => state.role || '未设置',
    hasUserInfo: (state) => state.isLoaded
  }
}); 
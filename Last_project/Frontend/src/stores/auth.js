import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const access = ref(localStorage.getItem('access') || '')
  const refresh = ref(localStorage.getItem('refresh') || '')
  const user = ref(null)

  const setTokens = (newAccess, newRefresh) => {
    access.value = newAccess
    refresh.value = newRefresh
    localStorage.setItem('access', newAccess)
    localStorage.setItem('refresh', newRefresh)
    axios.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
  }

  const setUser = (userData) => {
    user.value = userData
  }

  const fetchUser = async () => {
    try {
      const res = await axios.get('/api/accounts/user/', {
        headers: {
          Authorization: `Bearer ${access.value}`,
        },
      })
      user.value = res.data
    } catch (err) {
      console.error('❌ 유저 정보 요청 실패', err)
      throw err
    }
  }

  const logout = () => {
    access.value = ''
    refresh.value = ''
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    delete axios.defaults.headers.common['Authorization']
  }

  const refreshToken = async () => {
    if (!refresh.value) return

    try {
      const res = await axios.post('/api/token/refresh/', { refresh: refresh.value })
      setTokens(res.data.access, refresh.value)
    } catch (err) {
      console.error('리프레시 토큰 만료됨, 로그아웃 처리')
      logout()
    }
  }

  // 앱 시작 시 자동으로 refresh 시도 (자동 로그인 유지)
  if (refresh.value && !access.value) {
    refreshToken()
  } else if (access.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${access.value}`
  }

  return { access, refresh, user, setUser, setTokens, logout, refreshToken, fetchUser }
})

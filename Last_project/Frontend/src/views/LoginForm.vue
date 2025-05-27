<template>
  <div class="bg-black min-h-screen flex items-center justify-center py-20">
    <div class="w-full max-w-md bg-zinc-900 p-8 rounded-2xl shadow-2xl text-white">
      <h2 class="text-3xl font-bold mb-6 text-center text-white">로그인</h2>

      <form @submit.prevent="login" class="space-y-4">
        <input
          v-model="form.username"
          type="text"
          placeholder="아이디 (Username)"
          required
          class="w-full px-4 py-2 rounded-md bg-zinc-800 border border-zinc-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500"
        />
        <input
          v-model="form.password"
          type="password"
          placeholder="비밀번호 (Password)"
          required
          class="w-full px-4 py-2 rounded-md bg-zinc-800 border border-zinc-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500"
        />
        <button
          type="submit"
          class="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-md transition duration-200"
        >
          로그인
        </button>
      </form>

      <p v-if="errorMessage" class="text-red-400 text-sm mt-4 text-center">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({ username: '', password: '' })
const errorMessage = ref('')

const login = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/accounts/login/', form.value)
    const { access, refresh } = res.data
    authStore.setTokens(access, refresh)
    await authStore.fetchUser()
    alert('로그인 성공! 메인 페이지로 이동합니다.')
    router.push('/')
    errorMessage.value = ''
  } catch (err) {
    errorMessage.value = '아이디 또는 비밀번호가 틀렸습니다'
    console.error(err)
  }
}
</script>

<template>
  <div class="bg-black min-h-screen flex items-center justify-center py-20">
    <div class="w-full max-w-md bg-zinc-900 p-8 rounded-2xl shadow-2xl text-white">
      <h2 class="text-3xl font-bold mb-6 text-center text-white">회원가입</h2>

      <form @submit.prevent="signup" class="space-y-4">
        <input
          v-model="form.username"
          type="text"
          placeholder="사용자명 (Name)"
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
        <input
          v-model="form.password2"
          type="password"
          placeholder="비밀번호 확인 (Check Password)"
          required
          class="w-full px-4 py-2 rounded-md bg-zinc-800 border border-zinc-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500"
        />
        <input
          v-model="form.email"
          type="email"
          placeholder="이메일 (Email)"
          required
          class="w-full px-4 py-2 rounded-md bg-zinc-800 border border-zinc-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500"
        />

        <div class="flex items-center space-x-2">
          <input
            id="manager"
            type="checkbox"
            v-model="form.manager"
            class="w-4 h-4 text-red-600 bg-zinc-800 border-zinc-600 rounded focus:ring-red-500"
          />
          <label for="manager" class="text-sm text-gray-300">운영진 여부</label>
        </div>

        <select
          v-model="form.language"
          required
          class="w-full px-4 py-2 rounded-md bg-zinc-800 border border-zinc-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500"
        >
          <option value="" disabled selected>언어 선택 (Language)</option>
          <option value="ko">한국어</option>
          <option value="en">English</option>
          <option value="jp">日本語</option>
          <option value="cn">中文</option>
          <option value="es">Español</option>
        </select>

        <button
          type="submit"
          class="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-md transition duration-200"
        >
          회원가입
        </button>
      </form>

      <p v-if="errorMessage" class="text-red-400 text-sm mt-4 text-center">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const form = ref({
  username: '',
  password: '',
  password2: '',
  email: '',
  language: '',
  manager: false,
})
const errorMessage = ref('')

const signup = async () => {
  try {
    const res = await axios.post('/api/accounts/signup/', form.value)
    alert('회원가입 성공! 로그인 페이지로 이동할게요.')
    router.push('/login')
  } catch (err) {
    errorMessage.value = err.response?.data?.message || '회원가입 실패'
    console.error(err.response?.data)
  }
}
</script>

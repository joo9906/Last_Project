<template>
  <div class="h-screen">
    <nav class="fixed top-0 w-full z-50 bg-black bg-opacity-80 backdrop-blur-md shadow-md">
      <div class="container mx-auto flex items-center justify-between px-4 py-5">
        <div class="flex items-center space-x-6">
          <RouterLink to="/" class="text-white font-bold text-lg hover:text-red-500"
            >무비두루미</RouterLink
          >
          <!-- 데스크톱 메뉴 -->
          <ul class="hidden md:flex items-center space-x-6 text-sm text-white">
            <li><RouterLink to="/movies" class="hover:text-red-500">영화</RouterLink></li>
            <li><RouterLink to="/places" class="hover:text-red-500">촬영지</RouterLink></li>
            <li><RouterLink to="/tours" class="hover:text-red-500">투어 목록</RouterLink></li>
            <li><RouterLink to="/locationlog" class="hover:text-red-500">지도</RouterLink></li>
            <li v-if="isManager">
              <RouterLink to="/movies/create" class="hover:text-red-500">영화 등록</RouterLink>
            </li>
          </ul>
        </div>

        <!-- 오른쪽: 로그인/회원가입 -->
        <div class="hidden md:flex items-center space-x-6 text-sm text-white">
          <div class="hidden md:flex items-center">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="영화 또는 촬영지 검색"
              class="w-64 px-4 py-2 rounded bg-zinc-800 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500"
              @keyup.enter="handleSearch"
            />
            <button
              type="submit"
              class="bg-red-600 hover:bg-red-700 text-white font-semibold px-4 py-2 rounded ml-2"
              @click="handleSearch"
            >
              검색
            </button>
          </div>
          <template v-if="!isLoggedIn">
            <RouterLink to="/login" class="hover:text-red-500">로그인</RouterLink>
            <RouterLink to="/signup" class="hover:text-red-500">회원가입</RouterLink>
          </template>
          <template v-else>
            <RouterLink to="/mypage" class="hover:text-red-500">마이페이지</RouterLink>
            <RouterLink to="/logout" class="hover:text-red-500">로그아웃</RouterLink>
          </template>
        </div>

        <!-- 모바일 햄버거 버튼 -->
        <button
          @click="isMobileMenuOpen = !isMobileMenuOpen"
          class="md:hidden text-white focus:outline-none"
        >
          <svg
            v-if="!isMobileMenuOpen"
            class="h-6 w-6"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
          <svg
            v-else
            class="h-6 w-6"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- 모바일 메뉴 -->
      <div v-show="isMobileMenuOpen" class="md:hidden bg-black bg-opacity-95 backdrop-blur-md">
        <div class="flex justify-end items-center p-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="영화 또는 촬영지 검색"
            class="w-64 px-4 py-2 rounded bg-zinc-800 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500"
            @keyup.enter="handleSearch"
          />
          <button
            type="submit"
            class="bg-red-600 hover:bg-red-700 text-white font-semibold px-4 py-2 rounded ml-2"
            @click="handleSearch"
          >
            검색
          </button>
        </div>
        <div class="px-4 py-2 space-y-1">
          <RouterLink
            to="/movies"
            class="block text-white hover:text-red-500 py-2"
            @click="isMobileMenuOpen = false"
            >영화</RouterLink
          >
          <RouterLink
            to="/places"
            class="block text-white hover:text-red-500 py-2"
            @click="isMobileMenuOpen = false"
            >촬영지</RouterLink
          >
          <RouterLink
            to="/tours"
            class="block text-white hover:text-red-500 py-2"
            @click="isMobileMenuOpen = false"
            >투어 목록</RouterLink
          >
          <RouterLink
            to="/locationlog"
            class="block text-white hover:text-red-500 py-2"
            @click="isMobileMenuOpen = false"
            >지도</RouterLink
          >
          <RouterLink
            v-if="isManager"
            to="/movies/create"
            class="block text-white hover:text-red-500 py-2"
            @click="isMobileMenuOpen = false"
            >영화 등록</RouterLink
          >
          <template v-if="!isLoggedIn">
            <RouterLink
              to="/login"
              class="block text-white hover:text-red-500 py-2"
              @click="isMobileMenuOpen = false"
              >로그인</RouterLink
            >
            <RouterLink
              to="/signup"
              class="block text-white hover:text-red-500 py-2"
              @click="isMobileMenuOpen = false"
              >회원가입</RouterLink
            >
          </template>
          <template v-else>
            <RouterLink
              to="/mypage"
              class="block text-white hover:text-red-500 py-2"
              @click="isMobileMenuOpen = false"
              >마이페이지</RouterLink
            >
            <RouterLink
              to="/logout"
              class="block text-white hover:text-red-500 py-2"
              @click="isMobileMenuOpen = false"
              >로그아웃</RouterLink
            >
          </template>
        </div>
      </div>
    </nav>

    <!-- 메인 콘텐츠 영역 -->
    <main class="bg-black">
      <RouterView />
    </main>

    <!-- 검색 영역 -->
    <footer class="bg-black border-t border-gray-700 px-6 py-16">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-3xl font-bold mb-4 text-white">영화 또는 촬영지를 검색해보세요</h2>

        <form
          class="flex flex-col md:flex-row items-center justify-center gap-4"
          @submit.prevent="handleSearch"
        >
          <input
            v-model="searchQuery"
            type="text"
            placeholder="예: 부산행, 남산서울타워"
            class="w-full md:w-2/3 px-4 py-3 rounded bg-zinc-800 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500"
          />
          <button
            type="submit"
            class="bg-red-600 hover:bg-red-700 text-white font-semibold px-6 py-3 rounded"
          >
            검색
          </button>
        </form>

        <!-- 검색 결과 -->
        <div v-if="searchResults.length > 0" class="mt-8">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="result in searchResults"
              :key="result.id"
              class="bg-zinc-800 rounded-lg overflow-hidden"
            >
              <RouterLink
                :to="result.type === 'movie' ? `/movies/${result.id}` : `/places/${result.id}`"
              >
                <div class="p-4">
                  <img
                    :src="result.image"
                    :alt="result.title"
                    class="w-full h-48 object-cover rounded-lg mb-3"
                  />
                  <h3 class="text-white font-semibold text-lg mb-1">{{ result.title }}</h3>
                  <p class="text-gray-400 text-sm">
                    {{ result.type === 'movie' ? '영화' : '촬영지' }}
                  </p>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </footer>

    <footer class="bg-black text-white py-6 px-8">
      <div class="max-w-7xl mx-auto relative flex flex-col items-center space-y-1">
        <div class="absolute right-0 top-1/2 -translate-y-1/2 flex space-x-2">
          <a
            href="https://github.com/joo9906/Last_Project"
            target="_blank"
            rel="noopener noreferrer"
          >
            <div class="bg-gray-200 p-1 rounded">
              <img src="/github.png" alt="GitHub" class="w-7 h-7" />
            </div>
          </a>
          <a
            href="https://juvenile-flat-9b8.notion.site/1f82d7a9fb0080e69fbdccad0bf052c0?pvs=4"
            target="_blank"
            rel="noopener noreferrer"
          >
            <div class="bg-gray-200 p-1 rounded">
              <img src="/notion.jpg" alt="Notion" class="w-7 h-7 object-contain" />
            </div>
          </a>
        </div>

        <p class="text-sm opacity-70 text-center">
          &copy; 2025 왕주영, 권유진. All rights reserved.
        </p>
        <p class="text-sm opacity-70 text-center">SSAFY 13기 서울 파이썬 6반</p>
      </div>
    </footer>
  </div>

  <button
    @click="scrollToTop"
    :class="'fixed bottom-20 right-20 bg-red-600 hover:bg-red-700 text-white p-3 rounded-full shadow-lg transition duration-300 z-50 w-12 h-12 flex items-center justify-center'"
  >
    <img src="/upicon.png" alt="" />
  </button>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { RouterView, RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()
const user = authStore.user
const isLoggedIn = computed(() => !!authStore.access)
const isManager = computed(() => authStore.user?.manager === true)
const searchQuery = ref('')
const searchResults = ref([])
const isMobileMenuOpen = ref(false)

const handleSearch = () => {
  if (searchQuery.value.length < 2) {
    return
  }

  router.push({
    name: 'search',
    query: { q: searchQuery.value },
  })

  searchQuery.value = ''
  isMobileMenuOpen.value = false
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
}

onMounted(async () => {
  if (authStore.access) {
    try {
      await authStore.fetchUser()
    } catch (error) {
      console.error('족버그 발생:', error)
    }
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;700&family=Poppins:wght@300;400&display=swap');

body {
  font-family: 'Poppins', sans-serif;
}
</style>

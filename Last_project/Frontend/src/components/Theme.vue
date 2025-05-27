<template>
  <div class="font-montserrat text-sm bg-white dark:bg-zinc-900" :class="{ dark: isDark }">
    <!-- 모바일 네비게이션 바 -->
    <nav class="md:hidden fixed top-0 left-0 right-0 bg-white dark:bg-zinc-900 shadow-md z-50">
      <div class="flex items-center justify-between px-4 py-3">
        <div class="font-bold text-lg flex items-center gap-x-3">
          <svg class="h-8 w-8 fill-red-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M10 15.5v-7c0-.41.47-.65.8-.4l4.67 3.5c.27.2.27.6 0 .8l-4.67 3.5c-.33.25-.8.01-.8-.4Z" />
          </svg>
          <div class="tracking-wide dark:text-white">MMovie<span class="text-red-600">.</span></div>
        </div>
        <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <!-- 모바일 메뉴 -->
      <div v-if="isMobileMenuOpen" class="px-4 py-2 bg-white dark:bg-zinc-900 border-t border-gray-200 dark:border-zinc-700">
        <RouterLink
          v-for="item in navigation"
          :key="item.name"
          :to="item.href"
          class="block py-2 text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400"
          @click="isMobileMenuOpen = false"
        >
          {{ item.name }}
        </RouterLink>
      </div>
    </nav>

    <div class="flex min-h-screen 2xl:max-w-screen-2xl 2xl:mx-auto 2xl:border-x-2 2xl:border-gray-200 dark:2xl:border-zinc-700">
      <!-- 좌측 사이드바 (데스크톱) -->
      <aside class="w-1/6 py-10 pl-10 min-w-min border-r border-gray-300 dark:border-zinc-700 hidden md:block">
        <!-- 로고 -->
        <div class="font-bold text-lg flex items-center gap-x-3">
          <svg class="h-8 w-8 fill-red-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path
              d="M10 15.5v-7c0-.41.47-.65.8-.4l4.67 3.5c.27.2.27.6 0 .8l-4.67 3.5c-.33.25-.8.01-.8-.4Z"
            />
          </svg>
          <div class="tracking-wide dark:text-white">MMovie<span class="text-red-600">.</span></div>
        </div>

        <!-- 메뉴 -->
        <div class="mt-12 flex flex-col gap-y-4 text-gray-500 fill-gray-500 text-sm">
          <div class="text-gray-400/70 font-medium uppercase">Menu</div>
          <RouterLink
            v-for="item in navigation"
            :key="item.name"
            :to="item.href"
            :class="[
              route.path === item.href
                ? 'font-semibold text-red-600 border-r-4 border-r-red-600 pr-4 dark:text-white'
                : 'group hover:border-r-4 hover:border-r-red-600 hover:font-semibold dark:hover:text-white',
              'flex items-center space-x-2 py-1',
            ]"
          >
            <svg
              class="h-5 w-5 group-hover:fill-red-600"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
            >
              <path
                d="M4 6h16M4 12h16M4 18h16"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            <span>{{ item.name }}</span>
          </RouterLink>

          <!-- 다크모드 토글 -->
          <a class="flex items-center space-x-2 py-1 mt-4" href="#">
            <div
              class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in"
            >
              <input
                type="checkbox"
                id="toggle"
                class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 border-gray-300 appearance-none cursor-pointer"
                @click="isDark = !isDark"
                :checked="isDark"
              />
              <label
                for="toggle"
                class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"
              ></label>
            </div>
            <label for="toggle" class="text-sm text-gray-600 dark:text-white">Dark Theme</label>
          </a>
        </div>
      </aside>

      <!-- 메인 + 우측 사이드바 -->
      <main class="flex-1 flex">
        <!-- Main View -->
        <section class="flex-1 py-10 px-5 sm:px-10 md:mt-0 mt-16">
          <RouterView />

          <!-- 다크모드 전용 안내 -->
          <div v-if="isDark" class="mt-10 p-6 bg-zinc-800 text-white rounded-xl shadow-md">
            <h2 class="text-lg font-bold mb-2">🌙 다크모드 전용 안내</h2>
            <p class="text-sm">지금은 다크모드입니다. 눈이 편안하죠? 😎</p>
          </div>
        </section>

        <!-- Right Sidebar (검색창) -->
        <aside class="w-1/4 py-10 px-6 min-w-min border-l border-gray-300 dark:border-zinc-700 hidden lg:block">
          <div class="relative">
            <span class="text-gray-400 absolute left-4 top-3 cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input
              v-model="searchQuery"
              type="text"
              class="w-full pl-10 pr-4 py-2 rounded-full text-sm bg-transparent border ring-1 ring-gray-200 dark:ring-zinc-600 text-gray-700 dark:text-white focus:ring-red-300 focus:outline-none"
              placeholder="영화나 장소 검색..."
              @input="handleSearch"
            />
          </div>
          <!-- 검색 결과 -->
          <div v-if="searchResults.length > 0" class="mt-4">
            <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">검색 결과</h3>
            <div class="space-y-2">
              <div v-for="result in searchResults" :key="result.id" class="p-2 hover:bg-gray-100 dark:hover:bg-zinc-800 rounded cursor-pointer">
                <RouterLink :to="result.type === 'movie' ? `/movies/${result.id}` : `/places/${result.id}`">
                  <div class="flex items-center gap-2">
                    <img :src="result.image" :alt="result.title" class="w-10 h-10 object-cover rounded" />
                    <div>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ result.title }}</p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ result.type === 'movie' ? '영화' : '장소' }}</p>
                    </div>
                  </div>
                </RouterLink>
              </div>
            </div>
          </div>
        </aside>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import axios from 'axios'

const isDark = ref(false)
const authStore = useAuthStore()
const isLoggedIn = computed(() => !!authStore.access)
const route = useRoute()
const isMobileMenuOpen = ref(false)
const searchQuery = ref('')
const searchResults = ref([])

const navigation = computed(() =>
  isLoggedIn.value
    ? [
        { name: 'Home', href: '/' },
        { name: 'MovieList', href: '/movies/' },
        { name: 'MyMovie', href: '/favoritelist' },
        { name: 'Place', href: '/places' },
        { name: 'Location', href: '/locationlog' },
        { name: 'Tour', href: '/tours' },
        { name: 'Logout', href: '/logout' },
      ]
    : [
        { name: 'Home', href: '/' },
        { name: 'MovieList', href: '/movies/' },
        { name: 'Place', href: '/places' },
        { name: 'Location', href: '/locationlog' },
        { name: 'Tour', href: '/tours' },
        { name: 'Login', href: '/login' },
        { name: 'SignUp', href: '/signup' },
      ],
)

// 검색 기능
const handleSearch = async () => {
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    return
  }

  try {
    const [moviesRes, placesRes] = await Promise.all([
      axios.get(`/api/movies/search/?q=${searchQuery.value}`),
      axios.get(`/api/places/search/?q=${searchQuery.value}`)
    ])

    const movies = moviesRes.data.map(movie => ({
      ...movie,
      type: 'movie',
      image: movie.poster
    }))

    const places = placesRes.data.map(place => ({
      ...place,
      type: 'place',
      image: place.image
    }))

    searchResults.value = [...movies, ...places].slice(0, 5)
  } catch (error) {
    console.error('검색 중 오류 발생:', error)
    searchResults.value = []
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})

watch(isDark, (val) => {
  localStorage.setItem('theme', val ? 'dark' : 'light')
  document.documentElement.classList.toggle('dark', val)
})
</script>

<style scoped>
.toggle-checkbox:checked {
  @apply right-0 border-red-400;
  right: 0;
  border-color: #68d391;
}
.toggle-checkbox:checked + .toggle-label {
  @apply bg-red-400;
  background-color: #68d391;
}
</style>

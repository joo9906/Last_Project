<template>
  <div class="container mx-auto px-4 py-8 mt-16">
    <div class="max-w-4xl mx-auto">
      <!-- 프로필 섹션 -->
      <div class="bg-zinc-800 rounded-lg p-6 mb-8 shadow-lg">
        <div class="flex items-center space-x-4">
          <div class="w-20 h-20 bg-red-600 rounded-full flex items-center justify-center shadow-md">
            <span class="text-2xl text-white font-bold">{{
              user?.username?.[0]?.toUpperCase()
            }}</span>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white mb-1">{{ user?.username }}</h1>
            <p class="text-gray-400">{{ user?.email }}</p>
          </div>
        </div>
      </div>

      <!-- 즐겨찾기 영화 섹션 -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-white mb-4">즐겨찾기 영화</h2>
        <div
          v-if="favoriteMovies.length > 0"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          <div
            v-for="movie in favoriteMovies"
            :key="movie.id"
            class="bg-zinc-900 rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:scale-105 border border-zinc-700"
          >
            <RouterLink :to="`/movies/${movie.id}`">
              <div class="relative">
                <img
                  :src="movie.poster_url || movie.poster"
                  :alt="movie.title"
                  class="w-full h-64 object-cover"
                />
                <div
                  class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/80 to-transparent p-4"
                >
                  <h3 class="text-white font-semibold text-lg">{{ movie.title }}</h3>
                  <p class="text-gray-400 text-sm">{{ movie.release_year }}</p>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
        <p v-else class="text-gray-400 text-center py-8 bg-zinc-800 rounded-lg">
          즐겨찾기한 영화가 없습니다.
        </p>
      </div>

      <!-- 즐겨찾기 촬영지 섹션 -->
      <div>
        <h2 class="text-2xl font-bold text-white mb-4">즐겨찾기 촬영지</h2>
        <div
          v-if="visitedPlaces.length > 0"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          <div
            v-for="place in visitedPlaces"
            :key="place.id"
            class="bg-zinc-900 rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:scale-105 border border-zinc-700"
          >
            <RouterLink :to="`/places/${place.id}`">
              <div class="relative">
                <img
                  :src="place.image_url || place.image"
                  :alt="place.name"
                  class="w-full h-48 object-cover"
                />
                <div
                  class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/80 to-transparent p-4"
                >
                  <h3 class="text-white font-semibold text-lg">{{ place.name }}</h3>
                  <p class="text-gray-400 text-sm">{{ place.address }}</p>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
        <p v-else class="text-gray-400 text-center py-8 bg-zinc-800 rounded-lg">
          즐겨찾기한 촬영지가 없습니다.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const user = ref(null)
const favoriteMovies = ref([])
const visitedPlaces = ref([])

// ✅ 3. 유저 정보 불러오기 함수
const fetchUser = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/user/', {
      headers: {
        Authorization: `Bearer ${authStore.access || localStorage.getItem('access')}`,
      },
    })
    authStore.user = res.data
    user.value = res.data
  } catch (err) {
    console.error('유저 정보 불러오기 실패', err)
  }
}

// ✅ 4. 즐겨찾기 정보 불러오기
const fetchUserData = async () => {
  try {
    const token = authStore.access || localStorage.getItem('access')
    const favoritesRes = await axios.get('http://localhost:8000/api/favorites/', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    favoriteMovies.value = favoritesRes.data
      .filter((fav) => fav.movie)
      .map((fav) => ({
        ...fav.movie,
        poster_url: fav.movie.poster?.startsWith('http')
          ? fav.movie.poster
          : `http://localhost:8000${fav.movie.poster}`,
      }))

    const placeFavorites = favoritesRes.data.filter((fav) => fav.place)
    visitedPlaces.value = placeFavorites.map((fav) => ({
      ...fav.place,
      image_url: fav.place.image?.startsWith('http')
        ? fav.place.image
        : `http://localhost:8000${fav.place.image}`,
    }))
  } catch (error) {
    console.error('데이터 로딩 중 오류 발생:', error)
  }
}

// ✅ 5. onMounted에서 유저 정보 먼저 가져오고 나서 즐겨찾기 불러오기
onMounted(async () => {
  if (!authStore.user) {
    await fetchUser()
  } else {
    user.value = authStore.user
  }

  fetchUserData()
})
</script>

<style scoped>
.hover\:scale-105:hover {
  transform: scale(1.05);
}
</style>

<template>
  <div class="container mx-auto px-4 py-8 mt-16">
    <!-- 검색 결과 -->
    <div v-if="searchQuery && (movies.length > 0 || places.length > 0)" class="mb-8">
      <h1 class="text-3xl font-bold text-white mb-8">검색 결과: "{{ searchQuery }}"</h1>

      <!-- 영화 검색 결과 -->
      <div v-if="movies.length > 0" class="mb-12">
        <h2 class="text-2xl font-semibold text-white mb-4">영화</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="movie in movies"
            :key="movie.id"
            class="bg-zinc-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-transform duration-200"
          >
            <RouterLink :to="`/movies/${movie.id}`">
              <div class="relative">
                <img
                  :src="movie.poster_url || movie.poster"
                  :alt="movie.title"
                  class="w-full h-96 object-cover"
                />
                <div
                  class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4"
                >
                  <h3 class="text-white font-semibold text-lg">{{ movie.title }}</h3>
                  <p class="text-gray-300 text-sm">{{ movie.release_year }} • {{ movie.genre }}</p>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- 촬영지 검색 결과 -->
      <div v-if="places.length > 0">
        <h2 class="text-2xl font-semibold text-white mb-4">촬영지</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="place in places"
            :key="place.id"
            class="bg-zinc-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-transform duration-200"
          >
            <RouterLink :to="`/places/${place.id}`">
              <div class="relative">
                <img
                  :src="place.image_url || place.image"
                  :alt="place.name"
                  class="w-full h-64 object-cover"
                />
                <div
                  class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4"
                >
                  <h3 class="text-white font-semibold text-lg">{{ place.name }}</h3>
                  <p class="text-gray-300 text-sm">{{ place.address }}</p>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <!-- 검색 결과가 없을 때 -->
    <div v-else-if="searchQuery" class="text-center py-12">
      <p class="text-gray-400 text-lg">검색 결과가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const searchQuery = ref(route.query.q || '')
const movies = ref([])
const places = ref([])

const search = async () => {
  if (!searchQuery.value || searchQuery.value.length < 2) return

  try {
    const [moviesRes, placesRes] = await Promise.all([
      axios.get(
        `http://localhost:8000/api/movies/search/?q=${encodeURIComponent(searchQuery.value)}`,
      ),
      axios.get(
        `http://localhost:8000/api/places/search/?q=${encodeURIComponent(searchQuery.value)}`,
      ),
    ])

    movies.value = moviesRes.data.map((movie) => ({
      ...movie,
      poster_url: movie.poster?.startsWith('http')
        ? movie.poster
        : `http://localhost:8000${movie.poster}`,
    }))

    places.value = placesRes.data.map((place) => ({
      ...place,
      image_url: place.image?.startsWith('http')
        ? place.image
        : `http://localhost:8000${place.image}`,
    }))

    // URL 업데이트
    router.replace({
      query: { q: searchQuery.value },
    })
  } catch (error) {
    console.error('검색 중 오류 발생:', error)
    movies.value = []
    places.value = []
  }
}

const handleSearch = () => {
  search()
}

// URL 쿼리 파라미터 변경 감지
watch(
  () => route.query.q,
  (newQuery) => {
    if (newQuery) {
      searchQuery.value = newQuery
      search()
    }
  },
)

onMounted(() => {
  if (searchQuery.value) {
    search()
  }
})
</script>

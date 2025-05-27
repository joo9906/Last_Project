<template>
  <div class="container mx-auto px-4 py-8 mt-16">
    <div v-if="movie" class="bg-zinc-800 rounded-lg overflow-hidden">
      <!-- 영화 상세 정보 -->
      <div class="md:flex">
        <!-- 포스터 이미지 -->
        <div class="md:w-1/3">
          <img
            :src="getImageUrl(movie.poster)"
            class="w-full h-full object-cover"
            @error="handleImageError"
          />
        </div>

        <!-- 영화 정보 -->
        <div class="md:w-2/3 p-6">
          <div class="flex justify-between items-start">
            <h1 class="text-3xl font-bold text-white mb-2">{{ movie.title }}</h1>
            <!-- 즐겨찾기 버튼 -->
            <button
              @click="toggleFavorite"
              class="p-2 rounded-full transition-colors duration-200"
              :class="
                isFavorite ? 'text-red-500 hover:text-red-600' : 'text-gray-400 hover:text-gray-300'
              "
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                :fill="isFavorite ? 'currentColor' : 'none'"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                />
              </svg>
            </button>
          </div>

          <div class="flex items-center gap-4 text-gray-300 mb-4">
            <span>{{ movie.release_year }}</span>
            <span>•</span>
            <span>{{ movie.genre }}</span>
            <span>•</span>
            <span>{{ movie.runtime }}분</span>
          </div>

          <div class="mb-6">
            <h2 class="text-xl font-semibold text-white mb-2">줄거리</h2>
            <p class="text-gray-300">{{ movie.description }}</p>
          </div>

          <div class="mb-6">
            <h2 class="text-xl font-semibold text-white mb-2">감독</h2>
            <p class="text-gray-300">{{ movie.director }}</p>
          </div>

          <div class="mb-6">
            <h2 class="text-xl font-semibold text-white mb-2">출연</h2>
            <p class="text-gray-300">{{ movie.actors }}</p>
          </div>

          <div class="mb-6">
            <h2 class="text-xl font-semibold text-white mb-2">평점</h2>
            <div class="flex items-center">
              <div class="text-2xl font-bold text-yellow-400">{{ movie.score }}</div>
              <div class="text-gray-400 ml-2">/ 10</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 촬영지 목록 -->
      <div class="p-6 border-t border-gray-700">
        <h2 class="text-2xl font-semibold text-white mb-4">촬영지</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="place in moviePlaces"
            :key="place.id"
            class="bg-zinc-900 rounded-lg overflow-hidden"
          >
            <RouterLink :to="`/places/${place.id}`">
              <div class="relative">
                <img
                  :src="getImageUrl(place.image)"
                  :alt="place.name"
                  class="w-full h-48 object-cover"
                  @error="handleImageError"
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

    <!-- 추천 영화 목록 -->
    <div v-if="recommendedMovies.length" class="p-6 border-t border-gray-700">
      <h2 class="text-2xl font-semibold text-white mb-4">추천 영화</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <RouterLink
          v-for="rec in recommendedMovies"
          :key="rec.id"
          :to="`/movies/${rec.id}`"
          class="bg-zinc-900 rounded-lg overflow-hidden hover:shadow-lg transition"
        >
          <div class="relative">
            <img
              :src="getPosterUrl(rec.poster)"
              :alt="rec.title"
              class="w-full h-48 object-cover"
              @error="handleImageError"
            />
            <div class="p-4">
              <h3 class="text-lg font-bold text-white mb-1">{{ rec.title }}</h3>
              <p class="text-sm text-gray-400">유사도 점수: {{ rec.score }}</p>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-else class="text-center py-12">
      <p class="text-gray-400 text-lg">로딩 중...</p>
    </div>

    <MovieReview :movieId="movieId" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getRecommendList } from '@/api/recommend.js'
import axios from 'axios'
import MovieReview from '@/components/MovieReview.vue'

const route = useRoute()
const router = useRouter()
const movie = ref(null)
const moviePlaces = ref([])
const isFavorite = ref(false)
const authStore = useAuthStore()
const movieId = Number(route.params.id)
const recommendedMovies = ref([])
const altImage = '/images/alt_image copy.png'

watch(
  () => route.params.id,
  async (newId) => {
    if (newId) {
      await fetchMovieDetails()
      recommendedMovies.value = await getRecommendList(newId)
    }
  },
)

const fetchMovieDetails = async () => {
  try {
    const movieId = route.params.id
    console.log('Fetching movie details for ID:', movieId)

    // 영화 정보 가져오기
    const movieRes = await axios.get(`http://localhost:8000/api/movies/${movieId}/`)
    movie.value = movieRes.data
    console.log('Movie data:', movie.value)

    // 촬영지 정보 가져오기
    try {
      const placesRes = await axios.get(`http://localhost:8000/api/movies/${movieId}/places/`)
      moviePlaces.value = placesRes.data
      console.log('Places data:', moviePlaces.value)
    } catch (placeError) {
      console.error('촬영지 정보를 불러오는데 실패했습니다:', placeError)
      moviePlaces.value = []
    }

    // 즐겨찾기 상태 확인
    if (authStore.access) {
      try {
        const favoriteResponse = await axios.get('http://localhost:8000/api/favorites/', {
          headers: {
            Authorization: `Bearer ${authStore.access}`,
          },
        })
        isFavorite.value = favoriteResponse.data.some((fav) => fav.movie.id === movie.value.id)
      } catch (favoriteError) {
        console.error('즐겨찾기 상태 확인 실패:', favoriteError)
        isFavorite.value = false
      }
    }
  } catch (error) {
    console.error('영화 정보를 불러오는 중 오류 발생:', error)
    alert('영화 정보를 불러오는데 실패했습니다. 페이지를 새로고침해주세요.')
  }
}

onMounted(async () => {
  await fetchMovieDetails()
  recommendedMovies.value = await getRecommendList(movieId)
})

function getImageUrl(imagePath) {
  if (!imagePath) return '/images/alt_image copy.png'
  if (imagePath.startsWith('http')) return imagePath
  return `http://localhost:8000/media/${imagePath}`
}

function getPosterUrl(posterPath) {
  console.log('Poster path:', posterPath)
  if (!posterPath) return '/images/alt_image copy.png'
  if (posterPath.startsWith('http')) return posterPath
  // 경로에서 poster 숫자만 추출
  const posterNumber = posterPath.match(/poster(\d+)\.jpg/)?.[1]
  if (!posterNumber) return '/images/alt_image copy.png'
  return `http://localhost:8000/fixtures/posters/poster${posterNumber}.jpg`
}

function handleImageError(event) {
  event.target.src = '/images/alt_image copy.png'
}

const toggleFavorite = async () => {
  if (!authStore.access) {
    alert('로그인이 필요한 기능입니다.')
    return
  }

  try {
    if (isFavorite.value) {
      // 즐겨찾기 삭제
      const favoriteResponse = await axios.get('http://localhost:8000/api/favorites/', {
        headers: {
          Authorization: `Bearer ${authStore.access}`,
        },
      })
      const favorite = favoriteResponse.data.find((fav) => fav.movie.id === movie.value.id)
      if (favorite) {
        await axios.delete(`http://localhost:8000/api/favorites/${favorite.id}/`, {
          headers: {
            Authorization: `Bearer ${authStore.access}`,
          },
        })
      }
    } else {
      // 즐겨찾기 추가
      await axios.post(
        'http://localhost:8000/api/favorites/',
        { movie: movie.value.id },
        {
          headers: {
            Authorization: `Bearer ${authStore.access}`,
          },
        },
      )
    }
    isFavorite.value = !isFavorite.value
  } catch (error) {
    console.error('즐겨찾기 처리 중 오류가 발생했습니다:', error)
    alert('즐겨찾기 처리 중 오류가 발생했습니다.')
  }
}
</script>

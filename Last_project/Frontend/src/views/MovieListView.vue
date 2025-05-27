<template>
  <div class="page-container max-w-7xl mx-auto px-4 mt-10">
    <h1 class="text-3xl font-bold text-center text-white mb-10">영화 리스트</h1>

    <!-- 정렬 옵션 -->
    <div class="flex justify-end mb-6">
      <select
        v-model="sortOption"
        class="bg-zinc-800 text-white px-4 py-2 rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-red-500"
      >
        <option value="title">가나다순</option>
        <option value="score">평점순</option>
        <option value="release_year">개봉일순</option>
      </select>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <MovieCard
        v-for="movie in paginatedMovies"
        :key="movie.id"
        :movie="{
          title: movie.title,
          year: movie.release_year,
          poster: getPosterUrl(movie.poster),
          rating: movie.score,
          link: `/movies/${movie.id}`,
        }"
      />
    </div>

    <!-- 페이지네이션 -->
    <div class="flex justify-center mt-10 space-x-2">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="changePage(page)"
        :class="[
          'px-4 py-2 rounded-lg transition-colors duration-1',
          currentPage === page
            ? 'bg-red-600 text-white'
            : 'bg-zinc-800 text-gray-300 hover:bg-zinc-700',
        ]"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import MovieCard from '@/components/MovieCard.vue'

const movies = ref([])
const currentPage = ref(1)
const itemsPerPage = 16
const sortOption = ref('title')

// 정렬된 영화 목록
const sortedMovies = computed(() => {
  const sorted = [...movies.value]
  switch (sortOption.value) {
    case 'title':
      return sorted.sort((a, b) => a.title.localeCompare(b.title))
    case 'score':
      return sorted.sort((a, b) => b.score - a.score)
    case 'release_year':
      return sorted.sort((a, b) => b.release_year - a.release_year)
    default:
      return sorted
  }
})

// 현재 페이지의 영화만 보여주기
const paginatedMovies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return sortedMovies.value.slice(start, end)
})

// 전체 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(sortedMovies.value.length / itemsPerPage)
})

function getPosterUrl(posterPath) {
  if (!posterPath) return '/images/alt_image copy.png'
  if (posterPath.startsWith('http')) return posterPath
  const posterNumber = posterPath.match(/poster(\d+)\.jpg/)?.[1]
  if (!posterNumber) return '/images/alt_image copy.png'
  return `http://localhost:8000/fixtures/posters/poster${posterNumber}.jpg`
}

// 페이지 변경 함수
const changePage = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  fetch('http://localhost:8000/api/movies/')
    .then((res) => res.json())
    .then((data) => {
      movies.value = data
      console.log('🎬 Django 응답:', data)
    })
    .catch((err) => console.error('❌ Django fetch 에러:', err))
})
</script>

<style scoped>
  .page-container {
    padding-top: 80px; /* ✅ 네비게이션 바 공간 확보 */
  }
</style>

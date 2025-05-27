<template>
  <!-- 헤더 (비디오 배경 + 내비게이션) -->
  <header class="relative w-full h-[800px] overflow-hidden">
    <!-- 배경 영상 -->
    <div class="absolute inset-0 z-0 w-full h-full">
      <iframe
        src="https://www.youtube.com/embed/9jVZERSyDgw?autoplay=1&mute=1&loop=1&playlist=9jVZERSyDgw&controls=0&modestbranding=1"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen
        class="w-full h-full object-cover pointer-events-none"
      ></iframe>
    </div>

    <!-- 그라데이션 오버레이 -->
    <div
      class="absolute inset-0 z-10 bg-gradient-to-b from-transparent via-black/20 to-black"
    ></div>

    <!-- 텍스트 콘텐츠 -->
    <div
      class="relative z-20 container mx-auto px-4 md:px-16 h-full flex flex-col justify-end pb-16 opacity-80"
    >
      <div
        class="border-l border-white pl-4 sm:pl-6 md:pl-8 text-white p-6 sm:p-8 shadow-lg max-w-2xl"
        style="font-family: 'Hamlet', serif"
      >
        <p class="tracking-wide text-base sm:text-lg font-light mb-2">추천 영화</p>
        <h5 class="text-xl sm:text-3xl md:text-4xl lg:text-4xl font-bold mb-4">광해</h5>
        <p class="text-sm sm:text-md md:text-lg lg:text-xl text-gray-300 leading-relaxed mb-6">
          왕위를 둘러싼 권력 다툼과 붕당정치로 혼란이 극에 달한 광해군 8년. 자신의 목숨을 노리는
          자들에 대한 분노와 두려움으로 점점 난폭해져 가던 왕 '광해'는 도승지 '허균'에게 자신을
          대신하여 위협에 노출될 대역을 찾을 것을 지시한다. 이에 허균은 기방의 취객들 사이 ...
        </p>

        <RouterLink
          :to="`/movies/${movieId}`"
          class="btn-primary bg-zinc-700 hover:bg-zinc-600 text-white px-6 py-3 rounded inline-block text-base sm:text-lg"
        >
          영화 상세 보기
        </RouterLink>
      </div>

      <!-- 광해 촬영지 섹션 -->
      <div class="absolute bottom-8 right-8 w-1/3 z-30">
        <div class="bg-black bg-opacity-30 p-4 rounded-lg backdrop-blur-sm">
          <h2 class="text-2xl font-bold text-white mb-4 opacity-60 text-center">촬영지</h2>
          <div class="flex gap-4">
            <RouterLink
              v-for="place in placesForMovie81.slice(0, 2)"
              :key="place.id"
              :to="`/places/${place.id}`"
              class="block flex-1"
            >
              <div
                class="relative bg-zinc-900 rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:scale-105 border border-zinc-700"
              >
                <img
                  :src="getImageUrl(place.image)"
                  :alt="place.name"
                  class="w-full h-32 object-cover"
                  @error="handleImageError"
                />
                <div
                  class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/80 to-transparent p-2"
                >
                  <h3 class="text-white font-semibold text-xs">{{ place.name }}</h3>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- 투어 섹션 -->
  <section class="max-w-7xl mx-auto px-4 py-10">
    <h1
      class="text-3xl font-bold text-center text-gray-800 mb-10 text-white"
      style="font-family: 'Poppins', sans-serif"
    >
      투어 코스
    </h1>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <RouterLink
        v-for="route in tourRoutes.slice(0, 4)"
        :key="route.id"
        :to="`/tours/${route.id}`"
        class="block"
      >
        <div
          class="bg-zinc-900 rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:scale-105 border border-zinc-700"
        >
          <div class="relative">
            <img
              :src="`http://localhost:8000/fixtures/places/place${route.thumbnail_place_id}.jpg`"
              alt="썸네일"
              class="w-full h-48 object-cover"
              @error="handleImageError"
            />
            <div
              class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/80 to-transparent p-4"
            >
              <h3 class="text-white font-semibold text-lg">{{ route.name }}</h3>
              <p class="text-gray-400 text-sm">
                {{ formatDuration(route.total_duration || 0) }}
              </p>
            </div>
          </div>
        </div>
      </RouterLink>
    </div>
  </section>

  <!-- 추천 영화 섹션 -->
  <section class="max-w-7xl mx-auto px-4 py-10">
    <h1
      class="text-3xl font-bold text-center text-gray-800 mb-10 text-white"
      style="font-family: 'Poppins', sans-serif"
    >
      추천 영화
    </h1>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <MovieCard
        v-for="movie in movies.slice(0, 4)"
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
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import MovieCard from '@/components/MovieCard.vue'

const movieId = 81
const movies = ref([])
const places = ref([])
const tourRoutes = ref([])

// movieId (81) 에 해당하는 촬영지들만 필터
const placesForMovie81 = computed(() => places.value.filter((p) => p.movie === movieId))

function getPosterUrl(posterPath) {
  if (!posterPath) return '/images/alt_image copy.png'
  if (posterPath.startsWith('http')) return posterPath
  const posterNumber = posterPath.match(/poster(\d+)\.jpg/)?.[1]
  if (!posterNumber) return '/images/alt_image copy.png'
  return `http://localhost:8000/fixtures/posters/poster${posterNumber}.jpg`
}

function getImageUrl(imagePath) {
  return imagePath?.startsWith('http')
    ? imagePath
    : `http://localhost:8000/fixtures/places/${imagePath}`
}

function handleImageError(event) {
  event.target.src = '/images/alt_image.png'
}

function formatDuration(minutes) {
  const hrs = Math.floor(minutes / 60)
  const mins = minutes % 60
  return mins ? `${hrs}시간 ${mins}분` : `${hrs}시간`
}

onMounted(async () => {
  // 영화 데이터
  try {
    const res = await fetch('http://localhost:8000/api/movies/')
    const data = await res.json()
    movies.value = data.sort((a, b) => b.score - a.score)
  } catch (err) {
    console.error('Django fetch 에러:', err)
  }

  // 촬영지 데이터
  try {
    const res = await fetch('http://localhost:8000/api/places/')
    places.value = await res.json()
  } catch (err) {
    console.error('촬영지 데이터 에러:', err)
  }

  // 투어 코스 데이터
  try {
    const res = await fetch('http://localhost:8000/api/tour-routes/')
    tourRoutes.value = await res.json()
  } catch (err) {
    console.error('투어 코스 데이터 실패:', err)
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Hamlet&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Poppins&display=swap');

body {
  font-family: 'Hamlet', serif;
  font-family: 'Poppins', sans-serif;
}

/* Tailwind에 line-clamp 없을 경우 아래 추가 or plugin 설치 */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

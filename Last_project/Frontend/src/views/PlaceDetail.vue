<template>
  <div class="container mx-auto px-4 py-8 mt-16">
    <div v-if="place" class="bg-zinc-800 rounded-lg overflow-hidden shadow-lg">
      <!-- 기본 정보 -->
      <div class="md:flex">
        <div class="md:w-1/2">
          <img
            :src="getImageUrl(place.image)"
            :alt="place.name"
            class="w-full h-full object-cover"
          />
        </div>
        <div class="md:w-1/2 p-8">
          <h1 class="text-3xl font-bold text-white mb-6">{{ place.name }}</h1>
          <div class="mb-6">
            <h2 class="text-xl font-semibold text-white mb-2">주소</h2>
            <p class="text-gray-300">{{ place.address }}</p>
          </div>
          <div class="mb-6">
            <h2 class="text-xl font-semibold text-white mb-2">설명</h2>
            <p class="text-gray-300">{{ place.description }}</p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="toggleLike"
              class="flex items-center space-x-2 px-6 py-3 rounded-lg transition-colors duration-200 shadow-md"
              :class="
                isLiked ? 'bg-red-600 text-white' : 'bg-zinc-700 text-gray-300 hover:bg-zinc-600'
              "
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                :class="isLiked ? 'text-white' : 'text-gray-400'"
                fill="currentColor"
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
              <span class="font-semibold">{{ likeCount }}</span>
            </button>
          </div>
        </div>
      </div>
      <!-- 관련 영화 -->
      <div class="p-8 border-t border-gray-700">
        <h2 class="text-2xl font-bold text-white mb-6">관련 영화</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="movie in relatedMovies"
            :key="movie.id"
            class="bg-zinc-900 rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:scale-105 border border-zinc-700"
          >
            <RouterLink :to="`/movies/${movie.id}`">
              <div class="relative">
                <img
                  :src="getPosterUrl(movie.poster)"
                  :alt="movie.title"
                  class="w-full h-48 object-cover"
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
      </div>
      <!-- 🔹 관련 투어 코스 섹션 추가 -->
      <div v-if="relatedRoutes.length" class="p-8 border-t border-gray-700">
        <h2 class="text-2xl font-bold text-white mb-6">이 장소를 포함하는 투어 코스</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="route in relatedRoutes"
            :key="route.id"
            class="bg-zinc-900 rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:scale-105 border border-zinc-700"
          >
          <RouterLink
            :to="`/tours/${route.id}`"
            class="block bg-zinc-800 rounded-2xl shadow-md hover:shadow-lg transition p-4"
          >
            <img
                :src="`http://localhost:8000/fixtures/places/place${route.thumbnail_place_id}.jpg`"
                alt="썸네일"
                class="object-cover h-full w-full"
                @error="handleImageError"
            />
            <h3 class="text-xl font-semibold text-white mb-2">{{ route.name }}</h3>
            <!-- <p class="text-sm text-gray-400 mb-1 line-clamp-2">{{ route.description }}</p> -->
            <p class="text-xs text-gray-300">{{ formatDuration(route.total_duration) }}</p>
          </RouterLink>
          </div>
        </div>
      </div>

      <!-- 위치 정보 -->
      <div class="p-8 border-t border-gray-700">
        <h2 class="text-2xl font-bold text-white mb-6">위치</h2>
        <div id="map" class="w-full h-[450px] rounded-lg shadow-lg"></div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-else class="text-center py-12">
      <p class="text-gray-400 text-lg">로딩 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const place = ref(null)
const relatedMovies = ref([])
const isLiked = ref(false)
const likeCount = ref(0)
const authStore = useAuthStore()
let map = null
let marker = null

// 루트 추가
const relatedRoutes = ref([])

const formatDuration = minutes => {
  const hrs = Math.floor(minutes / 60)
  const mins = minutes % 60
  return mins ? `${hrs}시간 ${mins}분` : `${hrs}시간`
}

const handleImageError = (event) => {
        event.target.src = '/images/alt_image.png'
    }

const fetchPlaceDetail = async () => {
  try {
    const placeId = Number(route.params.id)
    console.log('Fetching place details for ID:', placeId)

    // 장소 정보 가져오기
    const placeRes = await axios.get(`http://localhost:8000/api/places/${placeId}/`)
    place.value = placeRes.data
    console.log('Place data:', place.value)

    // 관련 영화 정보 가져오기
    try {
      const moviesRes = await axios.get(`http://localhost:8000/api/places/${placeId}/movies/`)
      relatedMovies.value = moviesRes.data
      console.log('Movies data:', relatedMovies.value)
    } catch (movieError) {
      console.error('관련 영화 정보를 불러오는데 실패했습니다:', movieError)
      relatedMovies.value = []
    }

    // 투어정보 가져오기
   // 2-1) RoutePlace 전체 불러오기
   const { data: routePlaces } = await axios.get('http://localhost:8000/api/route-places/')
   // 2-2) 이 placeId를 포함하는 route ID들만 추출
   const routeIds = routePlaces
      .filter(rp => rp.place === placeId)
      .map(rp => rp.route)
   const uniqueRouteIds = [...new Set(routeIds)]
   // 2-3) TourRoute 전체 불러와서 필터링
   const { data: allRoutes } = await axios.get('http://localhost:8000/api/tour-routes/')
   relatedRoutes.value = allRoutes.filter(r => uniqueRouteIds.includes(r.id))


    // 즐겨찾기 상태 확인
    if (authStore.access) {
      try {
        const favoriteResponse = await axios.get(
          `http://localhost:8000/api/places/${placeId}/check-like/`,
          {
            headers: {
              Authorization: `Bearer ${authStore.access}`,
              'Content-Type': 'application/json',
            },
          },
        )
        isLiked.value = favoriteResponse.data.is_liked
        likeCount.value = favoriteResponse.data.like_count
        console.log('Favorite status:', { isLiked: isLiked.value, count: likeCount.value })
      } catch (favoriteError) {
        console.error('즐겨찾기 상태 확인 실패:', favoriteError)
        isLiked.value = false
        likeCount.value = 0
      }
    }

    // 카카오맵 초기화
    if (window.kakao && window.kakao.maps) {
      initMap()
    }
  } catch (error) {
    console.error('장소 정보를 불러오는 중 오류 발생:', error)
    alert('장소 정보를 불러오는데 실패했습니다. 페이지를 새로고침해주세요.')
  }
}

const toggleLike = async () => {
  if (!authStore.access) {
    alert('로그인이 필요한 기능입니다.')
    return
  }

  try {
    const response = await axios.post(
      `http://localhost:8000/api/places/${place.value.id}/toggle-like/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${authStore.access}`,
          'Content-Type': 'application/json',
        },
      },
    )

    isLiked.value = response.data.is_liked
    likeCount.value = response.data.like_count
  } catch (error) {
    console.error('즐겨찾기 처리 중 오류가 발생했습니다:', error)
    alert('즐겨찾기 처리 중 오류가 발생했습니다.')
  }
}

function getImageUrl(imagePath) {
  if (!imagePath) return ''
  return imagePath.startsWith('http')
    ? imagePath
    : `http://localhost:8000/media/places/${imagePath}`
}

function getPosterUrl(posterPath) {
  if (!posterPath) return ''
  return posterPath.startsWith('http') ? posterPath : `http://localhost:8000${posterPath}`
}

// 카카오맵 초기화 함수
const initMap = () => {
  if (!place.value || !place.value.latitude || !place.value.longitude) return

  const container = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(place.value.latitude, place.value.longitude),
    level: 3,
  }

  map = new kakao.maps.Map(container, options)

  // 마커 생성
  const markerPosition = new kakao.maps.LatLng(place.value.latitude, place.value.longitude)
  marker = new kakao.maps.Marker({
    position: markerPosition,
  })

  // 마커를 지도에 표시
  marker.setMap(map)

  // 인포윈도우 생성
  const infowindow = new kakao.maps.InfoWindow({
    content: `<div style="padding:5px;font-size:12px;">${place.value.name}</div>`,
  })
  
  let infoWindowOpen = false
  
  kakao.maps.event.addListener(marker, 'click', () => {
    if (infoWindowOpen) {
      infowindow.close()
    } else {
      infowindow.open(map, marker)
    }
    infoWindowOpen = !infoWindowOpen
  })
}

onMounted(() => {
  // 카카오맵 스크립트 로드
  if (!window.kakao || !window.kakao.maps) {
    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}`
    script.async = true
    script.onload = () => {
      fetchPlaceDetail()
    }
    document.head.appendChild(script)
  } else {
    fetchPlaceDetail()
  }
})

onUnmounted(() => {
  // 컴포넌트가 제거될 때 지도 인스턴스 정리
  if (map) {
    map = null
  }
  if (marker) {
    marker = null
  }
})
</script>

<style scoped>
  .hover\:scale-105:hover {
    transform: scale(1.05);
  }
</style>

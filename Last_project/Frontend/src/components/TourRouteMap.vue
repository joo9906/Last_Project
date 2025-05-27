<template>
  <!-- 지도 -->
  <div id="map" class="mx-auto w-[800px] h-[500px] rounded-lg shadow-md mb-6"></div>

  <!-- 5개 장소 리스트 -->
  <div v-if="nearestPlaces.length" class="max-w-3xl mx-auto">
    <ul class="space-y-4">
      <li
        v-for="place in nearestPlaces"
        :key="place.id"
        class="flex items-center p-4 bg-white rounded shadow hover:bg-gray-50 transition"
      >
        <RouterLink :to="`/places/${place.id}`" class="flex items-center space-x-4 w-full">
          <!-- 썸네일 -->
          <img
            :src="getImageUrl(place.image)"
            alt="썸네일"
            class="w-16 h-16 object-cover rounded"
          />
          <!-- 텍스트 -->
          <div class="flex-1">
            <p class="font-medium text-gray-800">{{ place.name }}</p>
            <p class="text-sm text-gray-500">{{ place.distance.toFixed(2) }} km</p>
          </div>
          <!-- 화살표 아이콘 -->
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'

const map = ref(null)
const userMarker = ref(null)
const placeMarkers = ref([])
const nearestPlaces = ref([])

// Kakao 스크립트 로드
function loadKakaoScript() {
  return new Promise((resolve) => {
    if (window.kakao?.maps) return resolve()
    const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=YOUR_KAKAO_APPKEY&autoload=false`
    script.onload = () => window.kakao.maps.load(resolve)
    document.head.appendChild(script)
  })
}

// 현재 위치 얻기
function getCurrentPosition() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      return reject(new Error('브라우저가 위치 정보를 지원하지 않습니다'))
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      (err) => reject(err),
      { enableHighAccuracy: true },
    )
  })
}

// 두 위경도 간 거리 계산 (Haversine)
function getDistance(lat1, lng1, lat2, lng2) {
  const toRad = (deg) => (deg * Math.PI) / 180
  const R = 6371 // 지구 반경 (km)
  const dLat = toRad(lat2 - lat1)
  const dLng = toRad(lng2 - lng1)
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c // km 단위 반환
}

// 이미지 URL 헬퍼
function getImageUrl(imagePath) {
  return imagePath.startsWith('http')
    ? imagePath
    : `http://localhost:8000/fixtures/places/${imagePath}`
}

onMounted(async () => {
  await loadKakaoScript()

  // 1) 사용자 위치
  let userLoc
  try {
    userLoc = await getCurrentPosition()
  } catch {
    userLoc = { lat: 37.554722, lng: 126.970833 } // 기본값
  }

  // 2) 지도 생성
  map.value = new kakao.maps.Map(document.getElementById('map'), {
    center: new kakao.maps.LatLng(userLoc.lat, userLoc.lng),
    level: 6,
  })

  // 3) 내 위치 마커
  const redIconUrl = '/my_location_marker.png' // 내 위치 아이콘 경로
  const markerImage = new kakao.maps.MarkerImage(redIconUrl, new kakao.maps.Size(64, 69), {
    offset: new kakao.maps.Point(27, 69),
  })

  userMarker.value = new kakao.maps.Marker({
    map: map.value,
    position: new kakao.maps.LatLng(userLoc.lat, userLoc.lng),
    title: '내 위치',
    image: markerImage, // ✅ 이미지 설정
  })

  // 4) 장소 데이터 불러오기
  let places = []
  try {
    const res = await axios.get('http://localhost:8000/api/places/')
    places = res.data
  } catch (e) {
    console.error('장소 목록 불러오기 실패', e)
    return
  }

  // 5) 거리 계산 및 가까운 5개 선택
  const nearest = places
    .map((p) => ({
      ...p,
      distance: getDistance(userLoc.lat, userLoc.lng, p.latitude, p.longitude),
    }))
    .sort((a, b) => a.distance - b.distance)
    .slice(0, 5)

  // 6) 지도에 마커 표시
  placeMarkers.value.forEach((m) => m.setMap(null))
  placeMarkers.value = nearest.map((p) => {
    const marker = new kakao.maps.Marker({
      map: map.value,
      position: new kakao.maps.LatLng(p.latitude, p.longitude),
      title: `${p.name} (${p.distance.toFixed(2)}km)`,
    })
    const iw = new kakao.maps.InfoWindow({
      content: `<div style="padding:8px; text-align:center;">
                  <strong>${p.name}</strong><br/>${p.distance.toFixed(2)} km
                </div>`,
    })
    let open = false
    kakao.maps.event.addListener(marker, 'click', () => {
      open ? iw.close() : iw.open(map.value, marker)
      open = !open
    })
    return marker
  })

  // 7) 내 위치와 5번째 장소 모두 보이도록 Bounds 조정
  const bounds = new kakao.maps.LatLngBounds()
  bounds.extend(new kakao.maps.LatLng(userLoc.lat, userLoc.lng))
  const fifth = nearest[4]
  bounds.extend(new kakao.maps.LatLng(fifth.latitude, fifth.longitude))
  map.value.setBounds(bounds)

  // 8) 리스트 렌더링용 데이터 채우기
  nearestPlaces.value = nearest
})
</script>

<style scoped>
.page-container {
  padding-top: 80px; /* 네비게이션 여백 */
}
</style>

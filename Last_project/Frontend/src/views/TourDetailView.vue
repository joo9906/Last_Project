<template>
  <div class="page-container">
    <section class="max-w-4xl mx-auto mt-10 px-4">
      <!-- 투어 정보 -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-white mb-4">{{ tour.name }}</h1>
        <p class="text-gray-400 text-lg mb-2">{{ formatDuration(tour.total_duration || 0) }}</p>
      </div>

      <!-- 장소 태그 -->
      <div v-if="placeNames.length" class="flex flex-wrap justify-center gap-2 mt-4">
        <span
          v-for="(name, idx) in placeNames"
          :key="idx"
          class="bg-zinc-800 text-white text-sm px-3 py-1 rounded-full border border-zinc-600"
        >
          {{ name }}
        </span>
      </div>

      <!-- 🗺 지도 -->
      <div class="col-span-3 mt-6 mb-10">
        <div id="map" class="w-full h-[500px] rounded-xl border border-gray-300 shadow-md"></div>
      </div>

      <!-- 장소 상세 설명 카드 (클릭 시 상세 페이지로) -->
      <RouterLink
        v-for="(rp, index) in routePlaces"
        :key="rp.id"
        :to="`/places/${rp.place}`"
        class="flex gap-6 items-start mb-8 bg-zinc-800 rounded-lg p-4 shadow hover:bg-zinc-700 transition"
      >
        <img
          :src="`http://localhost:8000/fixtures/places/place${rp.place}.jpg`"
          :alt="`place${rp.place}`"
          class="w-40 h-28 object-cover rounded border"
        />
        <div>
          <h2 class="text-xl font-semibold text-white mb-1">
            {{ index + 1 }}. {{ getPlace(rp.place)?.name }}
          </h2>
          <p class="text-sm text-gray-300">{{ getPlace(rp.place)?.address }}</p>
          <p class="text-sm text-gray-400 mt-2">{{ rp.description }}</p>
        </div>
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const tour = ref({})
const routePlaces = ref([])
const allPlaces = ref([])
const placeNames = ref([])

const formatDuration = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return mins ? `${hours}시간 ${mins}분` : `${hours}시간`
}

async function loadKakaoMapScript() {
  return new Promise((resolve) => {
    if (window.kakao?.maps) return resolve()
    const script = document.createElement('script')
    script.src = 'https://dapi.kakao.com/v2/maps/sdk.js?appkey=YOUR_KAKAO_API_KEY&autoload=false'
    script.async = true
    script.onload = () => window.kakao.maps.load(resolve)
    document.head.appendChild(script)
  })
}

function renderMap(points) {
  const container = document.getElementById('map')
  const bounds = new kakao.maps.LatLngBounds()
  const path = []

  const map = new kakao.maps.Map(container, {
    center: new kakao.maps.LatLng(points[0].lat, points[0].lng),
    level: 8,
  })

  points.forEach((p, idx) => {
    const position = new kakao.maps.LatLng(p.lat, p.lng)
    bounds.extend(position)
    path.push(position)

    const marker = new kakao.maps.Marker({
      map,
      position,
      title: `${idx + 1}. ${p.name}`,
    })

    const infoWindow = new kakao.maps.InfoWindow({
      content: `<div style="padding:8px;font-size:14px;"><strong>${idx + 1}. ${p.name}</strong><br/>${p.address}</div>`,
    })

    let infoWindowOpen = false

    kakao.maps.event.addListener(marker, 'click', () => {
      if (infoWindowOpen) {
        infoWindow.close()
      } else {
        infoWindow.open(map, marker)
      }
      infoWindowOpen = !infoWindowOpen
    })
  })

  const polyline = new kakao.maps.Polyline({
    path,
    strokeWeight: 4,
    strokeColor: '#FF5A5F',
    strokeOpacity: 0.8,
    strokeStyle: 'solid',
  })
  polyline.setMap(map)

  map.setBounds(bounds)
}

function getPlace(placeId) {
  return allPlaces.value.find((p) => p.id === placeId)
}

onMounted(async () => {
  try {
    const [tourRes, routePlaceRes, placeRes] = await Promise.all([
      axios.get(`http://localhost:8000/api/tour-routes/${route.params.id}/`),
      axios.get(`http://localhost:8000/api/route-places/`),
      axios.get(`http://localhost:8000/api/places/`),
    ])

    tour.value = tourRes.data
    const allRoutePlaces = routePlaceRes.data
    allPlaces.value = placeRes.data

    routePlaces.value = allRoutePlaces
      .filter((rp) => rp.route === tour.value.id)
      .sort((a, b) => a.order_index - b.order_index)

    const placeMap = Object.fromEntries(allPlaces.value.map((p) => [p.id, p.name]))
    placeNames.value = routePlaces.value.map((rp) => placeMap[rp.place])

    await loadKakaoMapScript()

    const points = routePlaces.value.map((rp) => {
      const place = allPlaces.value.find((p) => p.id === rp.place)
      return {
        lat: place.latitude,
        lng: place.longitude,
        name: place.name,
        address: place.address,
      }
    })

    if (points.length) renderMap(points)
  } catch (err) {
    console.error('데이터 로딩 실패:', err)
  }
})
</script>

<style scoped>
.page-container {
  padding-top: 80px;
}
#map {
  width: 100%;
  height: 500px;
}
</style>

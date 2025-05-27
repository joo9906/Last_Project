<template>
  <div class="page-container max-w-7xl mx-auto px-4 py-10">
    <h1 class="text-3xl font-bold text-center text-white mb-6">촬영지 리스트</h1>

    <!-- 지역 필터 태그: 6열 그리드 -->
    <div class="grid grid-cols-6 gap-x-2 gap-y-2 mb-8">
      <button
        v-for="region in regions"
        :key="region"
        @click="
          () => {
            selectedRegion = region
            currentPage = 1
          }
        "
        :class="[
          'px-3 py-1 rounded-full border transition',
          selectedRegion === region
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-zinc-800 text-gray-300 border-zinc-600 hover:bg-zinc-700',
        ]"
      >
        #{{ region }}
      </button>
    </div>

    <!-- 필터된 리스트 출력 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <PlaceCard
        v-for="place in paginatedPlaces"
        :key="place.id"
        :place="{
          name: place.name,
          address: place.address,
          description: place.description,
          image: getImageUrl(place.image),
          id: place.id,
        }"
        @error="handleImageError"
      />
    </div>

    <!-- 3️⃣ 페이지네이션: 6열 그리드 -->
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
import PlaceCard from '@/components/PlaceCard.vue'

const places = ref([])
const selectedRegion = ref('전체')

// 페이징 상태
const currentPage = ref(1)
const itemsPerPage = 12 // 한 페이지에 보여줄 아이템 수

// 1) API에서 데이터를 가져온 후 places 에 저장
onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/places/')
    places.value = await res.json()
  } catch (err) {
    console.error('장소 데이터 fetch 실패:', err)
  }
})

// 2) address의 첫 단어(지역)만 뽑아서 고유한 리스트를 만듦
const regions = computed(() => {
  const set = new Set(['전체'])
  places.value.forEach((p) => {
    const first = p.address?.split(' ')[0]
    if (first) set.add(first)
  })
  return Array.from(set)
})

// 3) selectedRegion 에 따라 places 필터링
const filteredPlaces = computed(() => {
  if (selectedRegion.value === '전체') {
    return places.value
  }
  return places.value.filter((p) => p.address.split(' ')[0] === selectedRegion.value)
})

// 4) 페이징된 결과
const paginatedPlaces = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredPlaces.value.slice(start, start + itemsPerPage)
})

// 5) 전체 페이지 수
const totalPages = computed(() => {
  return Math.ceil(filteredPlaces.value.length / itemsPerPage) || 1
})

// 6) 페이지 변경
function changePage(page) {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 7) 이미지 URL 헬퍼
function getImageUrl(imagePath) {
  if (!imagePath) return '/images/alt_image copy.png'
  if (imagePath.startsWith('http')) return imagePath
  const placeNumber = imagePath.match(/place(\d+)\.jpg/)?.[1]
  if (!placeNumber) return '/images/alt_image copy.png'
  return `http://localhost:8000/fixtures/places/place${placeNumber}.jpg`
}

// 8) 이미지 로드 실패 처리
function handleImageError(event) {
  event.target.src = '/images/alt_image copy.png'
}
</script>

<style scoped>
.page-container {
  padding-top: 80px; /* 네비 바 여유 */
}
</style>

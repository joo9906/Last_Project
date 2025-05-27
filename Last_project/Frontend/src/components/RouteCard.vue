<template>
  <router-link :to="`/tours/${route.id}`" class="block">
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
        <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/80 to-transparent p-4">
          <h3 class="text-white font-semibold text-lg">{{ route.name }}</h3>
          <p class="text-gray-400 text-sm">{{ formatDuration(route.total_duration) }}</p>
          <p class="text-xs text-gray-300 line-clamp-2 mt-1">{{ route.description }}</p>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  route: {
    type: Object,
    required: true
  }
})

const handleImageError = (event) => {
  event.target.src = '/images/alt_image copy.png'
}

const formatDuration = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  if (remainingMinutes === 0) {
    return `${hours}시간`
  }
  return `${hours}시간 ${remainingMinutes}분`
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
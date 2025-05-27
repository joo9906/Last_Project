<template>
  <router-link :to="`/places/${place.id}`" class="block">
    <div
      class="bg-zinc-900 rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:scale-105 border border-zinc-700"
    >
      <div class="relative">
        <img 
          :src="place.image" 
          @error="handleImageError" 
          class="w-full h-48 object-cover"
          :alt="place.name"
        />
        <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/80 to-transparent p-4">
          <h3 class="text-white font-semibold text-lg">{{ place.name }}</h3>
          <p class="text-gray-400 text-sm">{{ place.address }}</p>
          <p class="text-xs text-gray-300 line-clamp-2 mt-1">{{ place.description }}</p>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  place: {
    type: Object,
    required: true
  }
})

const handleImageError = (event) => {
  event.target.src = '/images/alt_image copy.png'
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
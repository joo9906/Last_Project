<template>
  <a :href="movie.link" class="block">
    <div
      class="bg-zinc-900 rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:scale-105 border border-zinc-700"
    >
      <div class="relative aspect-[2/3]">
        <img
          :src="movie.poster"
          :alt="movie.title"
          class="w-full h-full object-cover"
          @error="handleImageError"
        />
        <div
          class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/80 to-transparent p-4"
        >
          <h3 class="text-white font-semibold text-lg">{{ movie.title }}</h3>
          <p class="text-gray-400 text-sm">{{ movie.year }}년</p>
          <p class="text-xs text-gray-300">평점 {{ movie.rating }}</p>
        </div>
      </div>
    </div>
  </a>
</template>

<script setup>
defineProps({
  movie: {
    type: Object,
    required: true,
  },
})

const handleImageError = (event) => {
  event.target.src = '/images/alt_image copy.png'
}
</script>

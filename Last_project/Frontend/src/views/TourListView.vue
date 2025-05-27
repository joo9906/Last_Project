<template>
  <div class="page-container max-w-5xl mx-auto px-4 py-10">
    <h1 class="text-3xl font-bold text-center text-white mb-10">투어 리스트</h1>
    <div class="flex flex-col gap-6">
      <RouteCard v-for="route in routes" :key="route.id" :route="route" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import RouteCard from '@/components/RouteCard.vue'

const routes = ref([])

onMounted(() => {
  fetch('http://localhost:8000/api/tour-routes/')
    .then((res) => res.json())
    .then((data) => {
      routes.value = data
    })
    .catch((err) => console.error('투어 데이터 fetch 실패:', err))
})
</script>

<style scoped>
.page-container {
  padding-top: 80px;
}
</style>

<template>
  <div class="page-container">
    <div>
      <h1 class="text-3xl font-bold text-center text-white mb-10">내주위 촬영지</h1>
      <TourRouteMap :routeId="1" />
    </div>
  </div>
</template>

<script setup>
import TourRouteMap from '@/components/TourRouteMap.vue'
</script>

<style scoped>
  .page-container {
    padding-top: 80px; /* ✅ 네비게이션 바 공간 확보 */
  }
  h3 {
    color: #fff;
  }
</style>

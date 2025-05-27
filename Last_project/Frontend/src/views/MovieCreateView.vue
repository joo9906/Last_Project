<template>
  <div class="max-w-xl mx-auto my-40 bg-white p-8 rounded-lg shadow text-black">
    <h2 class="text-2xl font-bold mb-6 text-center">🎬 영화 등록</h2>
    <form @submit.prevent="submitMovie" class="space-y-4" enctype="multipart/form-data">
      <input v-model="form.title" placeholder="제목" required class="input" />
      <select v-model="form.genre" required class="input">
        <option value="">장르 선택</option>
        <option value="historical">사극</option>
        <option value="fantasy">판타지</option>
        <option value="action">액션</option>
        <option value="romance">멜로</option>
        <option value="horror">공포</option>
        <option value="crime">범죄</option>
        <option value="comedy">코미디</option>
        <option value="thriller">스릴러</option>
        <option value="drama">드라마</option>
        <option value="sci-fi">SF</option>
      </select>
      <input v-model="form.director" placeholder="감독" required class="input" />
      <input v-model="form.actors" placeholder="배우 (쉼표로 구분)" required class="input" />
      <input
        v-model.number="form.runtime"
        type="number"
        placeholder="상영시간 (분)"
        required
        class="input"
      />
      <input
        v-model.number="form.release_year"
        type="number"
        placeholder="개봉년도"
        required
        class="input"
      />
      <input
        v-model.number="form.score"
        type="number"
        step="0.5"
        min="0"
        max="10"
        placeholder="평점 (0-10점)"
        required
        class="input"
      />
      <textarea v-model="form.description" placeholder="설명" required class="input"></textarea>
      <input type="file" @change="handleFile" accept="image/*" required class="input" />
      <button type="submit" class="btn">등록하기</button>
      <p v-if="message" class="text-green-600">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  title: '',
  genre: '',
  director: '',
  actors: '',
  runtime: '',
  release_year: '',
  score: 2.5,
  description: '',
})
const file = ref(null)
const message = ref('')

const handleFile = (e) => {
  file.value = e.target.files[0]
}

const submitMovie = async () => {
  const formData = new FormData()

  // 데이터 형식 변환
  const movieData = {
    title: form.value.title,
    genre: form.value.genre,
    director: form.value.director,
    actors: form.value.actors,
    runtime: parseInt(form.value.runtime),
    release_year: parseInt(form.value.release_year),
    score: parseFloat(form.value.score),
    description: form.value.description,
  }

  // FormData에 데이터 추가
  Object.keys(movieData).forEach((key) => {
    formData.append(key, movieData[key])
  })

  if (file.value) {
    formData.append('poster', file.value)
  }

  console.log('전송할 데이터:', movieData)

  try {
    const response = await axios.post('/api/movies/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    console.log('서버 응답:', response.data)
    message.value = '영화 등록 성공!'
    form.value = {
      title: '',
      genre: '',
      director: '',
      actors: '',
      runtime: '',
      release_year: '',
      score: 2.5,
      description: '',
    }
    file.value = null
  } catch (err) {
    console.error('에러 상세:', err.response?.data)
    message.value = '등록 실패: ' + (err.response?.data?.detail || '알 수 없는 오류')
  }
}
</script>

<style scoped>
.input {
  @apply w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500;
}
.btn {
  @apply w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md font-bold;
}
</style>

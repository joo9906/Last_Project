import aixos from 'axios'

const API_URL = 'http://localhost:8000/api/movie_recommend/'

export async function getRecommendList(movieId) {
  try {
    const response = await aixos.get(`${API_URL}${movieId}/`)
    return response.data
  } catch (error) {
    console.error('추천 실패. 에러 내용용:', error)
    return [] // Re-throw the error for further handling if needed
  }
}

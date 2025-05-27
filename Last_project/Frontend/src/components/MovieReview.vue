<template>
  <div class="movie-review">
    <h3>리뷰</h3>
    
    <!-- 리뷰 작성 폼 -->
    <div v-if="isLoggedIn" class="review-form">
      <div class="rating-input">
        <label>평점:</label>
        <select v-model="newReview.rating">
          <option v-for="n in 5" :key="n" :value="n">{{ n }}점</option>
        </select>
      </div>
      <textarea
        v-model="newReview.content"
        placeholder="리뷰를 작성해주세요..."
        rows="4"
      ></textarea>
      <button @click="submitReview" class="submit-btn">리뷰 작성</button>
    </div>
    <div v-else class="login-message">
      리뷰를 작성하려면 <router-link to="/login">로그인</router-link>이 필요합니다.
    </div>

    <!-- 리뷰 목록 -->
    <div class="review-list">
      <div v-for="review in reviews" :key="review.id" class="review-item">
        <div class="review-header">
          <span class="username">{{ review.user.username }}</span>
          <span class="rating">⭐ {{ review.rating }}점</span>
          <span class="date">{{ formatDate(review.created_at) }}</span>
        </div>
        <p class="review-content">{{ review.content }}</p>
        <div v-if="isLoggedIn && review.user.id === currentUser.id" class="review-actions">
          <button @click="deleteReview(review.id)" class="delete-btn">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MovieReview',
  props: {
    movieId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      reviews: [],
      newReview: {
        content: '',
        rating: 5
      },
      isLoggedIn: false,
      currentUser: null
    }
  },
  created() {
    this.checkLoginStatus()
    this.fetchReviews()
  },
  methods: {
    async checkLoginStatus() {
      try {
        const response = await axios.get('/api/accounts/user/')
        this.isLoggedIn = true
        this.currentUser = response.data
      } catch (error) {
        this.isLoggedIn = false
        this.currentUser = null
      }
    },
    async fetchReviews() {
      try {
        const response = await axios.get(`/api/movies/${this.movieId}/reviews/`)
        this.reviews = response.data
      } catch (error) {
        console.error('리뷰를 불러오는데 실패했습니다:', error)
      }
    },
    async submitReview() {
      if (!this.newReview.content.trim()) {
        alert('리뷰 내용을 입력해주세요.')
        return
      }

      try {
        await axios.post(`/api/movies/${this.movieId}/reviews/`, this.newReview)
        this.newReview.content = ''
        this.newReview.rating = 5
        this.fetchReviews()
      } catch (error) {
        console.error('리뷰 작성에 실패했습니다:', error)
        alert('리뷰 작성에 실패했습니다.')
      }
    },
    async deleteReview(reviewId) {
      if (!confirm('정말로 이 리뷰를 삭제하시겠습니까?')) return

      try {
        await axios.delete(`/api/movies/${this.movieId}/reviews/${reviewId}/`)
        this.fetchReviews()
      } catch (error) {
        console.error('리뷰 삭제에 실패했습니다:', error)
        alert('리뷰 삭제에 실패했습니다.')
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.movie-review {
  margin: 2rem 0;
  color: #e5e5e5;
}

.movie-review h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #ffffff;
}

.review-form {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #1f2937;
  border-radius: 8px;
  border: 1px solid #374151;
}

.rating-input {
  margin-bottom: 1rem;
  color: #e5e5e5;
}

.rating-input select {
  margin-left: 0.5rem;
  padding: 0.5rem;
  background-color: #374151;
  color: #e5e5e5;
  border: 1px solid #4b5563;
  border-radius: 4px;
}

textarea {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  background-color: #374151;
  color: #e5e5e5;
  border: 1px solid #4b5563;
  border-radius: 4px;
  resize: vertical;
}

textarea::placeholder {
  color: #9ca3af;
}

.submit-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.submit-btn:hover {
  background-color: #2563eb;
}

.login-message {
  text-align: center;
  padding: 1.5rem;
  background-color: #1f2937;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #374151;
}

.login-message a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.login-message a:hover {
  text-decoration: underline;
}

.review-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-item {
  padding: 1.5rem;
  background-color: #1f2937;
  border-radius: 8px;
  border: 1px solid #374151;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
  color: #9ca3af;
}

.username {
  font-weight: 600;
  color: #e5e5e5;
}

.rating {
  color: #fbbf24;
}

.review-content {
  margin: 0.75rem 0;
  white-space: pre-wrap;
  color: #e5e5e5;
  line-height: 1.5;
}

.review-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.75rem;
}

.delete-btn {
  background-color: #dc2626;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.delete-btn:hover {
  background-color: #b91c1c;
}
</style> 
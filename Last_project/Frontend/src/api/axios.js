import axios from 'axios'

export default axios.create({
  baseURL: 'http://localhost:8000/api/', // Django 서버 주소
  headers: {
    'Content-Type': 'application/json',
  },
})

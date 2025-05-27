import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '../views/MainPageView.vue'
import MovieListView from '@/views/MovieListView.vue'
import PlaceDetail from '@/views/PlaceDetail.vue'
import PlaceListView from '@/views/PlaceListView.vue'
import TourDetailView from '@/views/TourDetailView.vue'
import TourListView from '@/views/TourListView.vue'
import LocationLogView from '@/views/LocationLogView.vue'
import FavoriteListView from '@/views/FavoriteListView.vue'
import LoginForm from '@/views/LoginForm.vue'
import SignUpForm from '@/views/SignUpForm.vue'
import { useAuthStore } from '@/stores/auth.js'
import SearchView from '@/views/SearchView.vue'
import MovieDetail from '@/views/MovieDetail.vue'
import MyPageView from '@/views/MyPageView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'mainpage',
      component: MainPageView,
    },
    {
      path: '/movies',
      name: 'movielist',
      component: MovieListView,
    },
    {
      path: '/movies/:id',
      name: 'moviedetail',
      component: MovieDetail,
    },
    {
      path: '/movies/create',
      name: 'moviecreate',
      component: () => import('@/views/MovieCreateView.vue'),
    },
    {
      path: '/places',
      name: 'placelist',
      component: PlaceListView,
    },
    {
      path: '/places/:id',
      name: 'placedetail',
      component: PlaceDetail,
    },
    {
      path: '/tours',
      name: 'tourlist',
      component: TourListView,
    },
    {
      path: '/tours/:id',
      name: 'tourdetail',
      component: TourDetailView,
    },
    {
      path: '/locationlog',
      name: 'locationlog',
      component: LocationLogView,
    },
    {
      path: '/favoritelist',
      name: 'favoritelist',
      component: FavoriteListView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginForm,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpForm,
    },
    {
      path: '/logout',
      name: 'logout',
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        authStore.logout()
        next('/login') // 로그아웃 후 로그인 페이지로 보냄
      },
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
      meta: { requiresAuth: true },
    },
  ],
})

export default router

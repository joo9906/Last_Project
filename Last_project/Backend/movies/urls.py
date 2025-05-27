from django.urls import path
from . import views
from .views import search_movies, search_places

urlpatterns = [
    # 영화 관련
    path('movies/', views.MovieListCreateView.as_view()),                # 전체 영화 목록 + 생성
    path('movies/<int:pk>/', views.MovieDetailView.as_view()),          # 영화 상세
    path('movies/create/', views.MovieCreateView.as_view(), name='movie-create'), # 영화 등록
    path('movies/<int:movie_id>/places/', views.movie_places, name='movie-places'), # 영화의 촬영지 목록

    # 장소 관련
    path('places/', views.PlaceListCreateView.as_view()),               # 장소 생성/목록
    path('places/<int:pk>/', views.PlaceDetailView.as_view()),          # 장소 상세

    # 영화-장소 연결
    path('movie-places/', views.MoviePlaceListCreateView.as_view()),
    path('movie-places/<int:pk>/', views.MoviePlaceDetailView.as_view()),
    path('movie-places/create/', views.create_movie_place, name='create-movie-place'),
    path('movie-places/<int:movie_id>/<int:place_id>/', views.delete_movie_place, name='delete-movie-place'),
    path('movie-places/movie/<int:movie_id>/', views.get_movie_places, name='get-movie-places'),

    # 투어 루트
    path('tour-routes/', views.TourRouteListCreateView.as_view()),      # 투어 루트 생성/목록
    path('tour-routes/<int:pk>/', views.TourRouteDetailView.as_view()), # 투어 루트 상세

    # 루트에 포함된 장소
    path('route-places/', views.RoutePlaceListCreateView.as_view()),
    path('route-places/<int:pk>/', views.RoutePlaceDetailView.as_view()),

    # 즐겨찾기
    path('favorites/', views.FavoriteListCreateView.as_view()),
    path('favorites/<int:pk>/', views.FavoriteDetailView.as_view()),

    # 위치 기반 로그
    path('location-logs/', views.LocationLogListCreateView.as_view()),
    path('location-logs/<int:pk>/', views.LocationLogDetailView.as_view()),

    path('movies/search/', search_movies, name='movie-search'),
    path('places/search/', search_places, name='place-search'),
    path('places/<int:place_id>/movies/', views.place_movies, name='place-movies'),
    path('places/<int:place_id>/check-like/', views.check_place_like, name='check-place-like'),
    path('places/<int:place_id>/toggle-like/', views.toggle_place_like, name='toggle-place-like'),
]

from rest_framework import generics
from .models import (
    Movie, Place, MoviePlace,
    TourRoute, RoutePlace,
    Favorite, LocationLog
)
from .serializers import (
    MovieSerializer, PlaceSerializer, MoviePlaceSerializer,
    TourRouteSerializer, RoutePlaceSerializer,
    FavoriteSerializer, LocationLogSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TourRoute, RoutePlace
from rest_framework.decorators import api_view
from django.db.models import Q


# Movie
class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
class MovieCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Place
class PlaceListCreateView(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

# MoviePlace
class MoviePlaceListCreateView(generics.ListCreateAPIView):
    queryset = MoviePlace.objects.all()
    serializer_class = MoviePlaceSerializer

class MoviePlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MoviePlace.objects.all()
    serializer_class = MoviePlaceSerializer

# TourRoute
class TourRouteListCreateView(generics.ListCreateAPIView):
    queryset = TourRoute.objects.all()
    serializer_class = TourRouteSerializer

class TourRouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourRoute.objects.all()
    serializer_class = TourRouteSerializer

# RoutePlace
class RoutePlaceListCreateView(generics.ListCreateAPIView):
    queryset = RoutePlace.objects.all()
    serializer_class = RoutePlaceSerializer

class RoutePlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoutePlace.objects.all()
    serializer_class = RoutePlaceSerializer

# Favorite
class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        movie_id = self.request.data.get('movie')
        place_id = self.request.data.get('place')
        route_id = self.request.data.get('route')

        if movie_id:
            movie = Movie.objects.get(id=movie_id)
            serializer.save(user=self.request.user, movie=movie)
        elif place_id:
            place = Place.objects.get(id=place_id)
            serializer.save(user=self.request.user, place=place)
        elif route_id:
            route = TourRoute.objects.get(id=route_id)
            serializer.save(user=self.request.user, route=route)
        else:
            serializer.save(user=self.request.user)

class FavoriteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

# LocationLog
class LocationLogListCreateView(generics.ListCreateAPIView):
    queryset = LocationLog.objects.all()
    serializer_class = LocationLogSerializer

class LocationLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationLog.objects.all()
    serializer_class = LocationLogSerializer



# 검색창에서 내용들을 받아올 함수
@api_view(['GET'])
def search_movies(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return Response([])
    
    movies = Movie.objects.filter(
        Q(title__icontains=query) |
        Q(director__icontains=query) |
        Q(actors__icontains=query) |
        Q(description__icontains=query)
    )[:5]
    
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_places(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return Response([])
    
    places = Place.objects.filter(
        Q(name__icontains=query) |
        Q(address__icontains=query) |
        Q(description__icontains=query)
    )[:5]
    
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_places(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        movie_places = MoviePlace.objects.filter(movie=movie)
        places = [mp.place for mp in movie_places]
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=404)

@api_view(['POST'])
def create_movie_place(request):
    try:
        movie_id = request.data.get('movie_id')
        place_id = request.data.get('place_id')
        scene_description = request.data.get('scene_description')

        if not all([movie_id, place_id, scene_description]):
            return Response({'error': '필수 필드가 누락되었습니다.'}, status=400)

        movie = Movie.objects.get(id=movie_id)
        place = Place.objects.get(id=place_id)

        movie_place = MoviePlace.objects.create(
            movie=movie,
            place=place,
            scene_description=scene_description
        )

        # Place 모델의 movie 필드도 업데이트
        place.movie = movie
        place.save()

        serializer = MoviePlaceSerializer(movie_place)
        return Response(serializer.data, status=201)
    except Movie.DoesNotExist:
        return Response({'error': '영화를 찾을 수 없습니다.'}, status=404)
    except Place.DoesNotExist:
        return Response({'error': '촬영지를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_movie_places(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        movie_places = MoviePlace.objects.filter(movie=movie)
        serializer = MoviePlaceSerializer(movie_places, many=True)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response({'error': '영화를 찾을 수 없습니다.'}, status=404)

@api_view(['DELETE'])
def delete_movie_place(request, movie_id, place_id):
    try:
        movie_place = MoviePlace.objects.get(movie_id=movie_id, place_id=place_id)
        movie_place.delete()
        return Response(status=204)
    except MoviePlace.DoesNotExist:
        return Response({'error': '연결을 찾을 수 없습니다.'}, status=404)

@api_view(['GET'])
def place_movies(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
        movie_places = MoviePlace.objects.filter(place=place)
        movies = [mp.movie for mp in movie_places]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Place.DoesNotExist:
        return Response({'error': '장소를 찾을 수 없습니다.'}, status=404)

@api_view(['GET'])
def check_place_like(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
        is_liked = Favorite.objects.filter(user=request.user, place=place).exists()
        like_count = Favorite.objects.filter(place=place).count()
        return Response({
            'is_liked': is_liked,
            'like_count': like_count
        })
    except Place.DoesNotExist:
        return Response({'error': '장소를 찾을 수 없습니다.'}, status=404)

@api_view(['POST'])
def toggle_place_like(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            place=place
        )
        
        if not created:
            favorite.delete()
            is_liked = False
        else:
            is_liked = True
            
        like_count = Favorite.objects.filter(place=place).count()
        
        return Response({
            'is_liked': is_liked,
            'like_count': like_count
        })
    except Place.DoesNotExist:
        return Response({'error': '장소를 찾을 수 없습니다.'}, status=404)



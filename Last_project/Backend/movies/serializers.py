from rest_framework import serializers
from .models import Movie, Place, MoviePlace, TourRoute, RoutePlace, Favorite, LocationLog, UserPrefer, MovieReview

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class MoviePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviePlace
        fields = '__all__'

class RoutePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePlace
        fields = '__all__'

class TourRouteSerializer(serializers.ModelSerializer):
    # 썸네일 이미지 id 가져오기기
    thumbnail_place_id = serializers.SerializerMethodField()
    # 연결된 place 가져오기
    route_places = RoutePlaceSerializer(many=True, read_only=True)

    class Meta:
        model = TourRoute
        fields = ['id', 'name', 'description', 'total_duration', 'created_at', 'thumbnail_place_id', 'route_places']

    def get_thumbnail_place_id(self, obj):
        first_place = RoutePlace.objects.filter(route=obj, order_index=1).first()
        if first_place and first_place.place:
            return first_place.place.id
        return None

class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    place = PlaceSerializer(read_only=True)
    route = TourRouteSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'movie', 'place', 'route']
        read_only_fields = ('user',)

class LocationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationLog
        fields = '__all__'

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrefer
        fields = '__all__'

class MovieReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = MovieReview
        fields = ['id', 'user', 'content', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username
        }
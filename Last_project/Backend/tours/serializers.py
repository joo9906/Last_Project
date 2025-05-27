from rest_framework import serializers
from .models import TourRoute, RoutePlace

class TourRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourRoute
        fields = '__all__'

class RoutePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePlace
        fields = '__all__'

from rest_framework import generics
from .models import TourRoute, RoutePlace
from .serializers import TourRouteSerializer, RoutePlaceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class TourRouteListCreateView(generics.ListCreateAPIView):
    queryset = TourRoute.objects.all()
    serializer_class = TourRouteSerializer

class TourRouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourRoute.objects.all()
    serializer_class = TourRouteSerializer

class RoutePlaceListCreateView(generics.ListCreateAPIView):
    queryset = RoutePlace.objects.all()
    serializer_class = RoutePlaceSerializer

class RoutePlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoutePlace.objects.all()
    serializer_class = RoutePlaceSerializer


# 루트를 json형식으로 반환하는 class
class RouteCoordinatesView(APIView):
    def get(self, request, pk):
        route = TourRoute.objects.get(pk=pk)
        places = RoutePlace.objects.filter(route=route).order_by('order_index')
        data = {
            "route_name": route.name,
            "places": [
                {
                    "name": p.place.name,
                    "lat": p.place.latitude,
                    "lng": p.place.longitude
                }
                for p in places
            ]
        }
        return Response(data)
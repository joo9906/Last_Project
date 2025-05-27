from rest_framework import generics
from .models import LocationLog
from .serializers import LocationLogSerializer

class LocationLogListCreateView(generics.ListCreateAPIView):
    queryset = LocationLog.objects.all()
    serializer_class = LocationLogSerializer

class LocationLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationLog.objects.all()
    serializer_class = LocationLogSerializer

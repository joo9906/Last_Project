from django.db import models
from django.conf import settings
from movies.models import Movie, Place

class LocationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logs_from_logsapp')
    latitude = models.FloatField()
    longitude = models.FloatField()
    detected_place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs_detected_place')
    recommended_movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs_recommended_movie')
    timestamp = models.DateTimeField(auto_now_add=True)


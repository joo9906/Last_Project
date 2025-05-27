from django.db import models
from django.conf import settings
from movies.models import Movie
from tours.models import TourRoute

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites_from_favapp')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='favorites_from_favapp')
    route = models.ForeignKey(TourRoute, on_delete=models.CASCADE, null=True, blank=True, related_name='favorites_from_favapp_routes')


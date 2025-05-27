from django.db import models
from django.conf import settings
from movies.models import Place

class TourRoute(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tour_routes_from_tourapp')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RoutePlace(models.Model):
    route = models.ForeignKey(TourRoute, on_delete=models.CASCADE, related_name='route_places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='route_places_from_tourapp')
    order_index = models.PositiveIntegerField()


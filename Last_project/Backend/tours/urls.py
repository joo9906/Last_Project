from django.urls import path
from . import views

urlpatterns = [
    path('', views.TourRouteListCreateView.as_view()),
    path('<int:pk>/', views.TourRouteDetailView.as_view()),
    path('route-places/', views.RoutePlaceListCreateView.as_view()),
    path('route-places/<int:pk>/', views.RoutePlaceDetailView.as_view()),
    path('tour-route/<int:pk>/coordinates/', views.RouteCoordinatesView.as_view())
]

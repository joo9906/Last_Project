from django.urls import path
from . import views

urlpatterns = [
    path('', views.FavoriteListCreateView.as_view()),
    path('<int:pk>/', views.FavoriteDetailView.as_view()),
]

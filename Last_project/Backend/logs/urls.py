from django.urls import path
from . import views

urlpatterns = [
    path('', views.LocationLogListCreateView.as_view()),
    path('<int:pk>/', views.LocationLogDetailView.as_view()),
]

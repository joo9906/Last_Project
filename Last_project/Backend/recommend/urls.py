from django.urls import path
from . import views

app_name = 'recommend'
urlpatterns = [
    path('<int:movie_id>/', views.recommend_by_id, name='recommend_by_title')
]

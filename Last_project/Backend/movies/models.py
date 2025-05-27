from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# 영화 정보 모델(제목, 장르, 개봉 연도, 설명, 포스터이미지 url)
class Movie(models.Model):
    GENRE_CHOICES = [
        ('historical', '사극'),
        ('fantasy', '판타지'),
        ('action', '액션'),
        ('romance', '멜로'),
        ('horror', '공포'),
        ('crime', '범죄'),
        ('comedy', '코미디'),
        ('thriller', '스릴러'),
        ('drama', '드라마'),
        ('sci-fi', 'SF'),
    ]
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    # 감독, 배우, 평점 추가, runtime
    director = models.CharField(max_length=255, default='')
    actors = models.CharField(max_length=255, default='')
    runtime = models.IntegerField()
    score = models.FloatField(default=2.5)
    release_year = models.IntegerField()
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# 장소(실제 존재하는 장소 정보 -> 주소, 경도, 위도, 설명 등등) + 여기에 사진을 넣어줄거임
class Place(models.Model):
    TYPE_CHOICES = [
        ('filming_location', 'Filming Location'),
        ('restaurant', 'Restaurant'),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='places/', default='/alt_image.png')

    # 영화제목 foreighnkey로 할거 저장
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='places', null=True, blank=True)

# 영화와 장소를 연결하는 모델, 어떤 장면에서 등장한것인지 설명하기 위한 scene_desc
class MoviePlace(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    scene_description = models.TextField()

# 사용자가 직접 만드는 투어 코스 -> 투어코스스
class TourRoute(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 다른사람에게 공개할지 여부. False일 경우 본인에게만 보임
    # is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_duration = models.IntegerField(blank=True, null=True)

# 어떤 장소들이 어떤 순서대로 들어가는지 들어있는 테이블
class RoutePlace(models.Model):
    route = models.ForeignKey(TourRoute, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    order_index = models.PositiveIntegerField()
    # 루트 설명 추가
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)  # 소요시간

# 본인이 좋아하는 영화와 루트를 저장
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    route = models.ForeignKey(TourRoute, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

# 현재 위치와 어떤 영화를 추천해줘야 할 지 판단하기 위한 정보가 담긴 필드
class LocationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    detected_place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    recommended_movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserPrefer(models.Model):
    Mood_choices = [
        ('happy', '행복'),
        ('sad', '슬픔'),
        ('angry', '분노'),
        ('fear', '두려움'),
        ('disgust', '혐오'),
        ('surprise', '놀람'),
    ]   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.CharField(max_length=20)
    mood = models.CharField(max_length=20, choices=Mood_choices)
    # created_at = models.DateTimeField(auto_now_add=True)

class MovieReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
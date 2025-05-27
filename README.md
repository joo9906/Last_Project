# 1. 팀원 정보 및 역할
## 권유진

## 왕주영
전체 프로젝트 총괄 및 프론트/백엔드 구현
역할 분담
발표 자료 작성, 발표
권유진 탈주 시도 저지

### 백엔드
-   모델 설정 및 테이블 구성
-   백엔드 서버 구축
-   model 및 serializer 구성, 데이터 전송 함수 전체 제작
-   영화 추천 알고리즘 구성 및 제작
-   로그인, 회원가입, 로그아웃 기능 제작

### 프론트엔드
-   router 설정
-   Component : Theme, MovieReview 제작
-   View : 뷰 전체 스켈레톤 제작, MainPage와 영화 관련 View 전체 제작, 카카오맵 API 사용, 검색 기능 구현현
-   테일윈드를 사용한 기본 UI 구성
-   영화, 촬영지 좋아요 기능
-   마이페이지 기능(좋아요 한 요소들 확인 가능)
-   데이터 삽입


# 2. 목표 서비스 구현 및 실제 구현 정도
## 목표 서비스
1. 한국 영화를 장르 기반으로 추천해주고 해당 영화의 촬영지 정보 제공
2. 제공된 촬영지를 기반으로 인근 투어 루트를 제공
3. 괜찮은 촬영지 / 영화는 즐겨찾기로 저장
4. 현재 위치 기반으로 장소 설명 + 해당 장소에서 촬영한 영화 추천
5. 로그인/로그아웃/회원가입 및 사용자 프로필 기능
6. 전체 영화 조회 시 정렬 기준 선택
7. 커뮤니티 기능을 리뷰로
8. 영화 검색 기능

## 구현 정도
1. 장르 기반 추천 대신 사용자가 특정 영화를 선택하면 그와 비슷한 영화를 자동으로 추천해주는 알고리즘으로 설정 -> TF-IDF 알고리즘 기반으로 더 고차원적 추천 기능 구현, 가장 유사한 5가지 영화 추천함
2. 특정 영화의 촬영지가 모여있는 투어 루트를 제공, 각 영화마다 촬영지 확인 가능
3. 촬영지 / 영화 즐겨찾기 기능 구현 및 마이페이지에서 선택 가능. 총 몇명이 즐겨찾기를 했는지도 확인 가능. 로그인 하지 않을 시 기능 막아놓음
4. 현재 위치 기반으로 인근의 촬영지 5개를 지도로 제공, 촬영지 클릭 시 관련된 영화 확인 가능
5. 로그인/로그아웃/회원가입/마이페이지 구현, 매니저 여부를 체크 가능하고 매니저일 경우 영화 등록 가능
6. 영화 정렬 기능 구현 완료
7. 각 영화별 리뷰 기능 구현
8. 영화 검색 기능 구현 완료

# 3. 데이터베이스 모델링 (ERD)
- 유저 : 이름, 이메일, 페스워드, 사용 언어, 매니저 여부
- 영화 : 제목, 장르, 개봉일, 줄거리, 배우, 감독, 상영시간, 평점, 포스터
- 영화 - 촬영지 연결 테이블 : 촬영 장면 설명, 영화 id, 촬영지 id
- 촬영지 : 이름, 타입, 주소, 위도, 경도, 설명, 영화 id, 촬영지 이미지지
- 영화 리뷰 : 내용, 평점, 생성시간, 업데이트 시간, 영화 id, 유저 id
- 즐겨찾기 : 영화 id, 루트 id, 유저 id, 촬영지 id
- 루트 : 촬영지 id, 루트 id, 설명 -> 권유진이 추가 입력할것
- 투어 루트 : -> 이것도 추가 입력

# 4. 영화 추천 알고리즘 설명
- TF-IDF + 코사인 유사도 기반 콘텐츠 기반 추천 시스템

```
from django.http import JsonResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movies.models import Movie

def recommend_by_id(request, movie_id):
    movies = Movie.objects.all()
    data = []

    for movie in movies:
        data.append({
            'id': movie.pk,
            'title': movie.title,
            'genre': movie.genre,
            'description': movie.description or '',
            'director': movie.director or '',
            'actors': movie.actors or '',
            'release_year': str(movie.release_year),
            'poster': movie.poster.url,
        })
		
		# 전처리
    df = pd.DataFrame(data)
    df['combined'] = df['title'] + ' ' + df['genre'] + ' ' + df['description'] + ' ' + df['director'] + ' ' + df['actors'] + ' ' + df['release_year']

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['combined'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    if movie_id not in df['id'].values:
        return JsonResponse({'error': '해당 ID의 영화 없음'}, status=404)

    idx = df[df['id'] == movie_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]

    result = [
        {
            'id': int(df.iloc[i]['id']),
            'title': df.iloc[i]['title'],
            'genre': df.iloc[i]['genre'],
            'poster': df.iloc[i]['poster'],
            'score': round(sim_scores[j][1], 3)
        }
        for j, i in enumerate(movie_indices)
    ]
    return JsonResponse(result, safe=False)
```

1. 전체 영화 데이터 불러오기
2. 각각의 영화의 id, title, genre, description, actors, release_year, poster 정보를 data 리스트에 넣은 다음 pd.DataFrame을 통해 표 형식으로 바꿔서 벡터화 준비
poster까지 넣은 이유 : 알고리즘을 통해 추천 영화를 만들었을 때 랜더링 하기 위해
3. 제목, 장르, 줄거리, 감독, 배우, 연도 등 모든 정보를 공백으로 이어서 한 줄로 만듦. → 텍스트 기반 벡터를 만들기 위한 전처리
4. TfidfVectorizer 함수를 사용해 상대적으로 의미가 있는 단어에 가중치를 부여(TF-IDF 알고리즘)
tfidf_matrix = n * M 크기의 희소 행렬.(n = 영화 수, m = 전체 단어 수)
5. `cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)` → 코사인 유사도 계산
6. 입력 영화 기준 유사도 비교

```jsx
idx = df[df['id'] == movie_id].index[0]
sim_scores = list(enumerate(cosine_sim[idx]))
sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
```

- idx = 추천 기준 영화
- sim_scores = idx 영화와 다른 영화와의 유사도 점수를 리스트에 넣고 높은 순서대로 배열(5개만)
7. result로 정리된 값들을 넣고 서버에서 result를 전송함

### 개선 가능성
- 	영화의 줄거리를 더 길게 하면 유사도 확인 수월
- 	추가 데이터를 삽입
- 	개인의 성향을 추가 데이터로 삽입하고 해당 데이터까지 고려

# 5. 핵심 기능에 대한 설명
1. 위치기반 서비스로 인근 촬영지 확인 기능
2. 영화 줄거리와 촬영지 등의 정보 확인
3. 관심있는 영화와 관련된 영화 추천 기능
4. 영화 및 촬영지 검색 기능


# 6. 생성형 AI를 활용한 부분
1. 카카오 API를 받아와서 랜더링 하는 부분
2. App.vue의 햄버거 버튼 부분
3. UI의 틀과 대략적인 부분을 만든 뒤 통일성을 위해 디자인을 일치하게 만듦
4. 투어 부분 구현이 어려운 것들
5. 영화 즐겨찾기는 구현했으나 촬영지 부분은 AI 사용, 마이페이지에서 동시에 받아 띄우는 부분

# 7. 느낀점, 후기
## 왕주영 
- 지금까지 해온 관통 프로젝트가 있어서 그나마 초반 부분을 수월하게 넘겼는데 실제로 서비스를 개발한다고 생각하면 아찔함. API를 받아와서 지도를 랜더링 하는 부분이 너무 헷갈려서 어려웠고 알고리즘을 작성 할 때에도 처음에는 movie의 정보들을 모두 따로 코사인 벡터를 비교하려고 하니 제대로 되지 않았고 AI의 도움을 받아 전체를 비교하며 유사도를 검증하는 방법을 알게 되었음.
- 몇 번을 해봐도 외래키 설정까지는 괜찮은데 중계 테이블을 만들어서 하는게 헷갈림.
- 중간중간에 버그가 터지는 부분을 잡아가면서 실력이 점점 늘어나는게 체감되었다고 생각함.
- 물론 끝까지 잡지 못한 버그는 남아있어서 매우 아쉬움.
- 원래 풀스택 개발자를 꿈꾸고 있었는데 하면 할수록 하나의 분야에 집중하는게 나을 것 같다고 생각.
- 생각보다 알고리즘을 개발하는 단계가 재미있었고 지금은 시간이 부족해서 못했지만 데이터가 더 많고 종류가 많은 상황에서 유사도 비교를 해보고싶다는 생각이 들었음.
- 가장 힘들었던 점은 데이터를 직접 만드는 것. API로 받아 올 수는 있었지만 외국 데이터이다 보니 정확하지 않았고 gpt가 json까지는 만든다고 하더라도 이미지를 직접 찾아오고 필요 없는 데이터를 전처리 하는 과정이 매우매우 귀찮았음.
- 기존에 bootstrap으로 ui를 구성하다가 tailwind를 사용하게 되었는데 자유도가 높은 만큼 확실히 내가 원하는대로 구현을 할 수 있어서 좋았음. 다만 높은 자유도 때문에 초반에 엄청 많이 헤맴
- 제일 어려운 점: 권유진 단도리하기

## 권유진 : 매주 관통 프로젝트에서 요구사항이 적을 때에는 몰랐는데 처음부터 ERD 작성하고 개발하려니깐 막막했다.
  수업을 따라서 구현하기만 했다가 직접 이름 만들고 불러오는 과정이 어려웠다.
  그래도 백엔드랑 프론트엔드 왔다갔다 하면서 구현하는 과정이 재밌었고 AI가 없던 개발자들은 어떻게 했을지 정말 대단하다는 생각을 했다. 백엔드보다는 프론트를 주로 했는데 렌더를 하는 과정에서 추가해야하는 필드도 생기고 중간에 수정되는 부분도 많더라. 기획자에 목표가 있었는데 기획자 아무나 하는게 아닌거 같다..

  데이터 만들기도 정말 노가다인걸 알았고,, 다음에는 더 시간을 쏟고 열심히 만들어서 더 완성도 높은 서비스 개발하고 싶다.

# 8. 배포 아직 안했는데 할라믄 깃허브로 하나? 나는 일단 내 티스토리에 올릴라고

# 9. 자유 작성성

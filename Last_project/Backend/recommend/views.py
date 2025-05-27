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

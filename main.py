# Keep only the relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'cast', 'keywords', 'crew']]

import ast

# Define the conversion functions for genres, cast, and crew
def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]

def convert3(obj):
    return [i['name'] for i in ast.literal_eval(obj)[:3]]

def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            return [i['name']]
    return []

# Apply conversion functions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Remove spaces from multi-word tags
for col in ['genres', 'keywords', 'cast', 'crew']:
    movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

# Create 'tags' column
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())

# Create a new DataFrame for recommendation system
new_df = movies[['movie_id', 'title', 'tags']]

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

for movie, vector in zip(movies, vectors):
    movie_vector = MovieVector(movie_id=movie.movie_id, vector=vector.tolist())
    session.merge(movie_vector)  # Use `merge` to avoid duplicate entries
session.commit()

def load_vectors():
    result = session.query(MovieVector).all()
    movie_ids = [mv.movie_id for mv in result]
    vectors = np.array([mv.vector for mv in result])
    return movie_ids, vectors

movie_ids, vectors = load_vectors()

# Calculate cosine similarity between movie vectors
similarity = cosine_similarity(vectors)

def recommend(movie):
    try:
        movie_index = new_df[new_df['title'].str.lower() == movie.lower()].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommendations = [new_df.iloc[i[0]].title for i in movies_list]
        return recommendations
    except IndexError:
        return ["Movie not found in the database."]

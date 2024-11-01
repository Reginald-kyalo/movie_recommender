#!/usr/bin/python3
import pandas as pd
from models import storage
from preprocessing import process_data
from nltk.stem.porter import PorterStemmer as ps
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))  # Stem each word
    return " ".join(y)  # Join the stemmed words

def recommend(movie):
    try:
        movies = process_data(movie)
    except Exception as e:
        return [e]

    ##Convert overview string to a list
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    
    # Remove spaces from multi-word tags
    for col in ['genres', 'keywords', 'cast', 'crew']:
        movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])
    
    # Create 'tags' column
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())
    
    # Create a new DataFrame for recommendation system
    new_df = movies[['movie_id', 'title', 'tags']]    
    
    # Apply stemming to the 'tags' column
    new_df['tags'] = new_df['tags'].apply(stem)
    
    # Vectorization - Convert text to numerical vectors
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    
    # Check the most frequent words (optional)
    # print(cv.get_feature_names_out())  # Updated method in sklearn >= 0.24
    
    # Calculate similarity using cosine similarity
    similarity = cosine_similarity(vectors)
    
    try:
        movie_index = new_df[new_df['title'].str.lower() == movie.lower()].index[0]
    except IndexError:
        return ["Movie not found in the database."]
    
    # Calculate distances and get the top 5 similar movies
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    # Retrieve recommended movie details
    recommendations = [movies.iloc[i[0]] for i in movies_list]
    recommendations_list = [rec.to_dict() for rec in recommendations]
    return recommendations_list

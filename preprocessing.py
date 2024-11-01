#!/usr/bin/python3
import ast
import json
import pandas as pd
from models import storage
from datetime import datetime
from models.movie import Movie
from models.credits import Credit
from models.movie_content_based import MovieContentBased

def parse_json_field(field):
    """Convert a JSON-like string to a list of dictionaries.
    """
    if pd.isna(field) or field.strip() == "":
        return []
    return ast.literal_eval(field)

def load_csv(csv_path):
    """Reads dataset from csv file
    and saves it to database
    """
    try:
        df = pd.read_csv(csv_path)
        df_cleaned = df.drop_duplicates().dropna()
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    csv_path = str(csv_path)
    path = csv_path.split('_')
    
    print(path)
    print(df_cleaned.head(5))
    if path[-1] == "movies.csv":
        for _, row in df_cleaned.iterrows():
            try:
                cls = 'Movie'
                if storage.get_item_by_id(cls, int(row['id'])):
                    print(f"Movie {row['title']} already exists in the database.")
                    continue

                movie = Movie(
                    movie_id=int(row['id']),
                    title=row['title'],
                    budget=int(row['budget']),
                    homepage=row['homepage'],
                    original_language=row['original_language'],
                    original_title=row['original_title'],
                    overview=row['overview'],
                    popularity=float(row['popularity']),
                    release_date=datetime.strptime(row['release_date'], "%Y-%m-%d"),
                    revenue=int(row['revenue']),
                    runtime=int(row['runtime']),
                    status=row['status'],
                    tagline=row['tagline'],
                    vote_average=float(row['vote_average']),
                    vote_count=int(row['vote_count']),
                    # Store list-like data as JSON strings
                    genres=str(parse_json_field(row['genres'])),
                    keywords=str(parse_json_field(row['keywords'])),
                    production_countries=str(parse_json_field(row['production_countries'])),
                    production_companies=str(parse_json_field(row['production_companies'])),
                    spoken_languages=str(parse_json_field(row['spoken_languages']))
                )
                movie.save()  # Save to the database
            except Exception as e:
                print(f"Error processing movie {row['title']}: {e}")

    # Handling credits.csv
    elif path[-1] == "credits.csv":
        for _, row in df_cleaned.iterrows():
            try:
                cls_1 = 'Credit'
                cls_2 = 'Movie'
                if storage.get_item_by_id(cls_1, int(row['movie_id'])):  # Assuming you have this method
                    print(f"Movie {row['title']} already exists in the database.")
                    continue
                if not storage.get_item_by_id(cls_2, int(row['movie_id'])):
                    print(f"Movie {row['title']} doesn't exist in the database.")
                    continue
                # Parse cast and crew JSON fields as text
                cast_text = json.dumps(parse_json_field(row['cast']))  # Convert to JSON string
                crew_text = json.dumps(parse_json_field(row['crew']))  # Convert to JSON string

                # Create a Credit object and save it to the database
                credit = Credit(
                    movie_id=int(row['movie_id']),
                    title=row['title'],
                    cast=cast_text,
                    crew=crew_text
                )
                credit.save()

            except Exception as e:
                print(f"Error processing credits for movie ID {row['movie_id']}: {e}")

    else:
        print("Unsupported file type. Please provide either 'movies.csv' or 'credits.csv'.")

def save_processed_data(movies_df):
    """Save the preprocessed movie data into the database."""
    cls = 'MovieContentBased'
    for _, row in movies_df.iterrows():
        if storage.get_item_by_id(cls, int(row['movie_id'])):  # Assuming you have this method
            print(f"Movie {row['title']} already exists in the database.")
            continue
        processed_movie = MovieContentBased(
            movie_id=row['movie_id'],
            title=row['title'],
            genres=row['genres'],
            keywords=row['keywords'],
            cast=row['cast'],
            director=row['crew'],
            overview=row['overview']
        )
        processed_movie.save()

def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]

def convert3(obj):
    return [i['name'] for i in ast.literal_eval(obj)[:3]]

def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            return [i['name']]
    return []

def load_processed_data():
    """Load preprocessed data from the database."""
    processed_set = storage.all('MovieContentBased')
    return pd.DataFrame([movie.to_dict() for movie in processed_set])

def process_data(movie_to_be_searched = None):
    """Data Preparation
    """
    movies = load_processed_data()
    if movies.empty:
        movies_set = storage.all('Movie')
        credits_set = storage.all('Credit')
        if not movies_set:
            try:
                load_csv("/home/reginald/reg_codes/webstack_portfolio_project/movie_recommender/tmdb_5000_movies.csv")
                movies_set = storage.all('Movie')
            except Exception as e:
                print(f"Error loading movies data: {e}")
        if not credits_set:
            try:
                load_csv("/home/reginald/reg_codes/webstack_portfolio_project/movie_recommender/tmdb_5000_credits.csv")
                credits_set = storage.all('Credit')
            except Exception as e:
                print(f"Error loading credits data: {e}")
        movies = pd.DataFrame([movie.to_dict() for movie in movies_set])
        credits = pd.DataFrame([credit.to_dict() for credit in credits_set])
        movies = movies.merge(credits,on='title')
        movies = movies.drop(columns=[col for col in movies.columns if col in ['_sa_instance_state_x', '_sa_instance_state_y', '__class___x', '__class___y', 'movie_id_y']])
        if 'movie_id_x' in movies.columns:
            movies = movies.rename(columns={'movie_id_x': 'movie_id'})
        print("Merged columns:", movies.columns)
        movies = movies[['movie_id', 'title', 'overview', 'genres', 'cast', 'keywords', 'crew']]
        movies['genres'] = movies['genres'].apply(convert)
        movies['keywords'] = movies['keywords'].apply(convert)
        movies['cast'] = movies['cast'].apply(convert3)
        movies['crew'] = movies['crew'].apply(fetch_director)
        save_processed_data(movies)
    if movie_to_be_searched:
        if not movies[movies['title'].str.lower() == movie_to_be_searched.lower()].any().any():
            raise IndexError("Movie not found in the database.")

    return movies
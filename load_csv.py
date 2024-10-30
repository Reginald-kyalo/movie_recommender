#!/usr/bin/python3
import os
import pandas as pd
import ast
import json
from shlex import split
from datetime import datetime
from models.movie import Movie
from models.credits import Credit
from models import storage

def parse_json_field(field):
    """Convert a JSON-like string to a list of dictionaries.
    """
    if pd.isna(field) or field.strip() == "":
        return []  # Handle missing or empty fields
    return ast.literal_eval(field)

def do_load(csv_path):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        df_cleaned = df.drop_duplicates().dropna()
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Determine which file is being loaded based on the filename
    csv_path = str(csv_path)
    path = csv_path.split('_')

    # Handling movies.csv
    if path[-1] == "movies.csv":
        for _, row in df_cleaned.iterrows():
            try:
                if storage.get_item_by_id(int(row['id'])):  # Assuming you have this method
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
                    production_companies=str(parse_json_field(row['production_companies'])),
                    production_countries=str(parse_json_field(row['production_countries'])),
                    spoken_languages=str(parse_json_field(row['spoken_languages']))
                )
                movie.save()  # Save to the database
            except Exception as e:
                print(f"Error processing movie {row['title']}: {e}")

    # Handling credits.csv
    elif path[-1] == "credits.csv":
        for _, row in df_cleaned.iterrows():
            try:
                if storage.get_item_by_id(int(row['movie_id'])):  # Assuming you have this method
                    print(f"Movie {row['title']} already exists in the database.")
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

def main():
    try:
        do_load('/home/reginald/reg_codes/webstack_portfolio_project/movie_recommender/i_movies.csv')
    except Exception as e:
        print(f"Error loading CSV: {e}")

if __name__ == "__main__":
    main()
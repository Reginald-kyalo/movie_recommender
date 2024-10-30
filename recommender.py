#!/usr/bin/python3
import pandas as pd
from models import storage

# Load data from the 'movies' and 'credits' tables into DataFrames
movies = storage.all('Movie')
credits = storage.all('Credit')

# Merge movies and credits on 'movie_id'
movies = movies.merge(credits, on='movie_id')

movies.head(5)

#!/usr/bin/python3
"""Defines the MovieContentBased class for content-based filtering.

The MovieContentBased class represents a movie within the content-based 
recommendation system, storing essential attributes that aid in generating 
personalized movie recommendations based on genres, keywords, cast, and director.
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Text

class MovieContentBased(BaseModel, Base):
    """Representation of the MovieContentBased class.

    This class inherits from BaseModel and Base, representing movies
    in a content-based filtering context. Each instance stores essential
    movie attributes for recommendation processing, including genres,
    keywords, cast, and director.

    Attributes:
        __tablename__ (str): Name of the table in the database.
        movie_id (int): Primary key representing the unique ID of a movie.
        title (str): Title of the movie, must be unique.
        overview (str): Brief description or overview of the movie plot.
        genres (str): Comma-separated genres associated with the movie.
        keywords (str): Comma-separated keywords describing the movie.
        cast (str): Comma-separated cast members of the movie.
        director (str): Name of the movie's director.
    """
    __tablename__ = 'movies_content_based'
    movie_id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    overview = Column(String)
    genres = Column(Text)
    keywords = Column(Text)
    cast = Column(Text)
    director = Column(Text)

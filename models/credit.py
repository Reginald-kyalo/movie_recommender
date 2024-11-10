#!/usr/bin/python3
"""Defines the Credit class, representing movie credits information.

This module provides the Credit class, which stores information about the cast and crew of a movie.
Each Credit instance is associated with a specific movie in the database.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

class Credit(BaseModel, Base):
    """Represents a movie's credits, including cast and crew information.

    Attributes:
        movie_id (int): The ID of the associated movie, serving as a foreign key.
        title (str): The title of the movie.
        cast (str): JSON-like string containing information about the cast members.
        crew (str): JSON-like string containing information about the crew members.
        movie (relationship): Relationship to the Movie class, allowing access to the associated movie.
    """

    __tablename__ = 'credits'

    movie_id = Column(Integer, ForeignKey('movies.movie_id', ondelete='CASCADE'), primary_key=True)
    title = Column(Text)
    cast = Column(Text)
    crew = Column(Text)

    movie = relationship("Movie", backref="credits")

#!/usr/bin/python3
from models.base_model import BaseModel, Base
from models.movie import Movie
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Date, Numeric, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

class MovieVector(BaseModel, Base):
    __tablename__ = 'movie_vectors'
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
    vector = Column(ARRAY(Float), nullable=False)

    movie = relationship('Movie', back_populates='vector')

Movie.vector = relationship('MovieVector', uselist=False, back_populates='movie')

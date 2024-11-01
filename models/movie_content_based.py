#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Text

class MovieContentBased(BaseModel, Base):
    __tablename__ = 'movies_content_based'
    movie_id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    overview = Column(String)
    genres = Column(Text)
    keywords = Column(Text)
    cast = Column(Text)
    director = Column(Text)

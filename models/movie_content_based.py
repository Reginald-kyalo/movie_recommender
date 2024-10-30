#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import relationship

class MovieContentBased(BaseModel, Base):
    __tablename__ = 'movies_content_based'
    movie_id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    overview = Column(String)
    genres = Column(Text)
    keywords = Column(Text)
    cast = Column(Text)
    crew = Column(Text)

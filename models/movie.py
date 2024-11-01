#!/usr/bin/python3
"""Movie ORM Model
"""
import pandas as pd
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, Text, Date, Numeric

class Movie(BaseModel, Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    budget = Column(Numeric)
    genres = Column(Text)
    homepage = Column(Text)
    keywords = Column(Text)
    original_language = Column(String(10))
    original_title = Column(Text)
    overview = Column(Text)
    popularity = Column(Float)
    production_companies = Column(Text)
    production_countries = Column(Text)
    release_date = Column(Date)
    revenue = Column(Numeric)
    runtime = Column(Float)
    spoken_languages = Column(Text)
    status = Column(String(20))
    tagline = Column(Text)
    vote_average = Column(Float)
    vote_count = Column(Integer)
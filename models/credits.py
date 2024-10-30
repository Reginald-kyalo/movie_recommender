#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

class Credit(BaseModel, Base):
    __tablename__ = 'credits'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id', ondelete='CASCADE'))
    title = Column(Text)
    cast = Column(Text)
    crew = Column(Text)

    movie = relationship("Movie", backref="credits")

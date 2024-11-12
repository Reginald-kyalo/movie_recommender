#!/usr/bin/python3
"""Database storage engine for the movie recommendation system.

This module provides the DBStorage class, which manages the database connection,
session, and data manipulation for SQLAlchemy models in the movie recommendation system.
"""

from models.base_model import Base
from models.credit import Credit
from models.movie import Movie
from models.movie_content_based import MovieContentBased
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from dotenv import load_dotenv
from urllib.parse import urlparse

class DBStorage:
    """Database storage engine for handling data persistence with SQLAlchemy models.

    Attributes:
        __engine (sqlalchemy.Engine): The SQLAlchemy engine instance.
        __session (sqlalchemy.Session): The current SQLAlchemy session instance.
    """

    __engine = None
    __session = None

    def __init__(self) -> None:
        """Initializes an instance of DBStorage.

        Loads environment variables and sets up a SQLAlchemy engine to
        connect to the PostgreSQL database. Uses SSL mode for secure connection.
        """
        load_dotenv()
        tmpPostgres = urlparse(getenv("DATABASE_URL"))
        self.__engine = create_engine(
            f"postgresql://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?sslmode=require",
            echo=True
        )

    def all(self, cls):
        """Query all objects of a given class from the current database session..

        Args:
            cls (type or str): The class of objects to query. If None, all classes are queried.

        Returns:
            dict: A dictionary with queried classes in the format <class name> = obj.
        """
        if cls is None:
            objs = self.__session.query(Movie).all()
            objs.extend(self.__session.query(Credit).all())
            objs.extend(self.__session.query(MovieContentBased).all())
        else:
            if type(cls) == str:
                try:
                    cls = eval(cls)
                except NameError:
                    return {}
            objs = self.__session.query(cls).all()
        return {obj for obj in objs}

    def get_item_by_id(self, cls, id):
        """Retrieve an item by class and ID from the database.

        Args:
            cls (type or str): The class of the item to retrieve.
            id (int): The ID of the item to retrieve.

        Returns:
            obj: The item instance if found, otherwise None.
        """
        if id is None:
            return None
        if type(cls) == str:
            cls = eval(cls)
        return self.__session.query(cls).filter(cls.movie_id == id).first()

    def new(self, obj):
        """Add an object to the current database session.

        Args:
            obj (Base): The object instance to add to the session.
        """
        self.__session.add(obj)

    def delete(self, obj=None):
        """Delete an object from the current database session.

        Args:
            obj (Base, optional): The object instance to delete from the session.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and start a new session.

        Initializes the SQLAlchemy session by binding it to the engine.
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def save(self):
        """Commit all changes in the current database session."""
        self.__session.commit()

    def close(self):
        """Close the current database session."""
        self.__session.close()

#1/usr/bin/python3
from models.base_model import BaseModel, Base
from models.credits import Credit
from models.movie import Movie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """Sets up attributes and methods for storage
    for mapping hbnb instances to database
    Returns:
        engine (sqlalchemy.Engine): working SQLAlchmey Engine
        session (sqlalchemy.Session): working SQLAlchemy Session
    """

    __engine = None
    __session = None

    def __init__(self) -> None:
        """Initializes an instance of DBStorage"""
        DB_URL = getenv("DATABASE_URL")
        self.__engine = create_engine(DB_URL, pool_pre_ping=True)
        ##if getenv("HBNB_ENV") == "test":
        ##    Base.metadata.drop_all(self.__engine)
    def all(self, cls):
        """Query on the curret database session all objects of the given class.

        If cls is None, queries all types of objects.

        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self.__session.query(Movie).all()
            objs.extend(self.__session.query(Credit).all())
            ##objs.extend(self.__session.query(User).all())
            ##objs.extend(self.__session.query(Place).all())
            ##objs.extend(self.__session.query(Review).all())
            ##objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {o for o in objs}
    
    def get_item_by_id(self, cls, id):
        if type(cls) == str:
            cls = eval(cls)
        return self.__session.query(cls).filter(cls.movie_id == id).first()

    def new(self, obj):
        """adds objects to current database session"""
        self.__session.add(obj)

    def delete(self, obj=None):
        """delete from the current
        database session obj if not None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def close(self):
        """closes current database session """
        self.__session.close()
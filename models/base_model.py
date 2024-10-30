#!/usr/bin/python3
import models
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel():
    """Represents the BaseModel of the Movie recommender project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                self.__dict__[k] = v

    def save(self):
        """Update updated_at with the current datetime."""
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        models.storage.delete(self)
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        rdict = self.__dict__.copy()
        rdict["__class__"] = str(type(self).__name__)
        return rdict

    def __str__(self):
        """Return the print/str representation of the BaseModel instance.
        """
        d = self.__dict__.copy()
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)
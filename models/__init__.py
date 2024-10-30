"""Instantiates a storage object.
"""
from models.engine.db_storage import DBStorage
storage = DBStorage()
storage.reload()
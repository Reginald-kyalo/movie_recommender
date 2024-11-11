#!/usr/bin/python3
""" """
import unittest
from unittest.mock import patch, MagicMock
from models.engine.db_storage import DBStorage
from models.movie import Movie
from models.credit import Credit
from models.movie_content_based import MovieContentBased

class TestDBStorage(unittest.TestCase):
    """ """
    @patch('models.db_storage.create_engine')
    @patch('models.db_storage.scoped_session')
    @patch('models.db_storage.urlparse')
    @patch('models.db_storage.getenv')
    def setUp(self, mock_getenv, mock_urlparse, mock_scoped_session, mock_create_engine):
        """ """
        mock_getenv.return_value = 'postgresql://user:pass@localhost/testdb'
        mock_urlparse.return_value.username = 'user'
        mock_urlparse.return_value.password = 'pass'
        mock_urlparse.return_value.hostname = 'localhost'
        mock_urlparse.return_value.path = '/testdb'
        self.storage = DBStorage()
        self.storage.__session = MagicMock()

    def test_all_with_class(self):
        """ """
        mock_session = self.storage.__session
        mock_session.query().all.return_value = [Movie(id=1), Movie(id=2)]
        result = self.storage.all('Movie')
        self.assertIn("Movie.1", result)
        self.assertIn("Movie.2", result)

    def test_all_without_class(self):
        """ """
        mock_session = self.storage.__session
        mock_session.query(Movie).all.return_value = [Movie(id=1)]
        mock_session.query(Credit).all.return_value = [Credit(movie_id=1)]
        mock_session.query(MovieContentBased).all.return_value = [MovieContentBased(movie_id=1)]
        result = self.storage.all(None)
        self.assertIn("Movie.1", result)
        self.assertIn("Credit.1", result)
        self.assertIn("MovieContentBased.1", result)

    def test_get_item_by_id(self):
        """ """
        mock_session = self.storage.__session
        mock_movie = Movie(id=1)
        mock_session.query().filter().first.return_value = mock_movie
        result = self.storage.get_item_by_id('Movie', 1)
        self.assertEqual(result, mock_movie)

    def test_get_item_by_id_not_found(self):
        """ """
        mock_session = self.storage.__session
        mock_session.query().filter().first.return_value = None
        result = self.storage.get_item_by_id('Movie', 999)
        self.assertIsNone(result)

    def test_new(self):
        """ """
        mock_session = self.storage.__session
        movie = Movie(id=3)
        self.storage.new(movie)
        mock_session.add.assert_called_once_with(movie)

    def test_delete(self):
        """ """
        mock_session = self.storage.__session
        movie = Movie(id=4)
        self.storage.delete(movie)
        mock_session.delete.assert_called_once_with(movie)

    def test_delete_none(self):
        """ """
        mock_session = self.storage.__session
        self.storage.delete(None)
        mock_session.delete.assert_not_called()

    def test_reload(self):
        """ """
        with patch('models.db_storage.Base.metadata.create_all') as mock_create_all, \
             patch('models.db_storage.scoped_session') as mock_scoped_session:
            self.storage.reload()
            mock_create_all.assert_called_once_with(self.storage._DBStorage__engine)
            mock_scoped_session.assert_called_once()

    def test_save(self):
        """ """
        mock_session = self.storage.__session
        self.storage.save()
        mock_session.commit.assert_called_once()

    def test_close(self):
        """ """
        mock_session = self.storage.__session
        self.storage.close()
        mock_session.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()

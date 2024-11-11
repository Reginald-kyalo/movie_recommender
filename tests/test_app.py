#!/usr/bin/python3
""" """
import unittest
from unittest.mock import patch
from app import app

class TestRecommendationEndpoint(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.recommend')
    def test_recommend_successful_response(self, mock_recommend):
        """ """
        mock_recommend.return_value = {"recommendations": ["Movie A", "Movie B", "Movie C"]}
        response = self.app.get('/recommend?title=inception')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"recommendations": ["Movie A", "Movie B", "Movie C"]})

    def test_recommend_missing_title(self):
        """ """
        response = self.app.get('/recommend')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Movie Title is required."})

    @patch('app.recommend')
    def test_recommend_no_recommendations_found(self, mock_recommend):
        """ """
        mock_recommend.return_value = ["No recommendations found for the given title."]
        response = self.app.get('/recommend?title=unknownmovie')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "No recommendations found for the given title."})

    @patch('app.recommend')
    def test_recommend_unexpected_error(self, mock_recommend):
        """ """
        mock_recommend.return_value = None
        response = self.app.get('/recommend?title=inception')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "An unexpected error occurred"})

if __name__ == '__main__':
    unittest.main()

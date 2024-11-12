import unittest
from unittest.mock import patch
from ..recommender import stem, recommend
import pandas as pd

class TestMovieRecommender(unittest.TestCase):
    def test_stem(self):
        text = "connections connecting connected"
        expected_result = "connect connect connect"
        self.assertEqual(stem(text), expected_result, "Stemming not applied correctly")

    @patch('movie_recommender.process_data')
    def test_recommend(self, mock_process_data):
        mock_data = pd.DataFrame({
            'movie_id': [1, 2, 3, 4, 5, 6],
            'title': ["Inception", "Interstellar", "Memento", "Batman Begins", "The Prestige", "Dunkirk"],
            'genres': [["Sci-Fi", "Action"], ["Sci-Fi", "Adventure"], ["Mystery"], ["Action"], ["Drama"], ["War"]],
            'keywords': [["dream", "subconscious"], ["space", "wormhole"], ["memory"], ["hero"], ["illusion"], ["battle"]],
            'cast': [["Leonardo DiCaprio"], ["Matthew McConaughey"], ["Guy Pearce"], ["Christian Bale"], ["Hugh Jackman"], ["Tom Hardy"]],
            'director': [["Christopher Nolan"], ["Christopher Nolan"], ["Christopher Nolan"], ["Christopher Nolan"], ["Christopher Nolan"], ["Christopher Nolan"]],
            'overview': ["A thief who steals corporate secrets...", "A team of explorers travel through...", "A man with short-term memory loss...", "After training with his mentor...", "Two stage magicians engage...", "Allied soldiers are surrounded..."]
        })
        
        mock_process_data.return_value = mock_data
        
        result = recommend("Inception")
        self.assertIsInstance(result, list, "Result should be a list")
        self.assertTrue(len(result) > 0, "Recommendations should not be empty")
        self.assertIn("title", result[0], "Each recommendation should contain 'title' field")
        
        result_not_found = recommend("Non Existent Movie")
        self.assertEqual(result_not_found, ["Movie not found in the dataframe."], "Should return 'Movie not found' for unknown titles")

    @patch('movie_recommender.process_data')
    def test_recommend_error_handling(self, mock_process_data):
        mock_process_data.side_effect = Exception("Processing error")
        result = recommend("Inception")
        self.assertEqual(result, ["Processing error"], "Should return the exception message on error")

if __name__ == '__main__':
    unittest.main()

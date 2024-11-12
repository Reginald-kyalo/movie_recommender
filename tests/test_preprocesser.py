#!/usr/bin/python3
""" """
import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
from preprocesser import (
    parse_json_field,
    load_csv,
    save_processed_data,
    convert,
    convert3,
    fetch_director,
    load_processed_data,
    process_data
)

class TestPreprocesser(unittest.TestCase):
    """ """
    def test_parse_json_field_valid_json(self):
        """ """
        input_str = '[{"id": 28, "name": "Action"}]'
        expected_output = [{"id": 28, "name": "Action"}]
        result = parse_json_field(input_str)
        self.assertEqual(result, expected_output, "Should correctly parse valid JSON string")

    def test_parse_json_field_empty_string(self):
        """ """
        input_str = ''
        expected_output = []
        result = parse_json_field(input_str)
        self.assertEqual(result, expected_output, "Should return empty list for empty string")

    def test_parse_json_field_nan(self):
        """ """
        input_str = pd.NA
        expected_output = []
        result = parse_json_field(input_str)
        self.assertEqual(result, expected_output, "Should return empty list for NaN input")

    def test_parse_json_field_invalid_json(self):
        """ """
        input_str = 'invalid json'
        with self.assertRaises(ValueError):
            parse_json_field(input_str)

    def test_convert_valid_input(self):
        """ """
        input_str = '[{"name": "Action"}, {"name": "Adventure"}]'
        expected_output = ["Action", "Adventure"]
        result = convert(input_str)
        self.assertEqual(result, expected_output, "Should extract list of names from JSON-like string")

    def test_convert_empty_list(self):
        """ """
        input_str = '[]'
        expected_output = []
        result = convert(input_str)
        self.assertEqual(result, expected_output, "Should return empty list when input is empty")

    def test_convert_invalid_input(self):
        """ """
        input_str = 'invalid'
        with self.assertRaises(ValueError):
            convert(input_str)

    def test_convert3_valid_input(self):
        """ """
        input_str = '[{"name": "Actor1"}, {"name": "Actor2"}, {"name": "Actor3"}, {"name": "Actor4"}]'
        expected_output = ["Actor1", "Actor2", "Actor3"]
        result = convert3(input_str)
        self.assertEqual(result, expected_output, "Should return first three names from JSON-like string")

    def test_convert3_less_than_three(self):
        """ """
        input_str = '[{"name": "Actor1"}, {"name": "Actor2"}]'
        expected_output = ["Actor1", "Actor2"]
        result = convert3(input_str)
        self.assertEqual(result, expected_output, "Should return available names when less than three")

    def test_convert3_empty_input(self):
        """ """
        input_str = '[]'
        expected_output = []
        result = convert3(input_str)
        self.assertEqual(result, expected_output, "Should return empty list for empty input")

    def test_fetch_director_present(self):
        """ """
        input_str = '[{"name": "Director1", "job": "Director"}, {"name": "Producer1", "job": "Producer"}]'
        expected_output = ["Director1"]
        result = fetch_director(input_str)
        self.assertEqual(result, expected_output, "Should extract director's name when present")

    def test_fetch_director_absent(self):
        """ """
        input_str = '[{"name": "Producer1", "job": "Producer"}]'
        expected_output = []
        result = fetch_director(input_str)
        self.assertEqual(result, expected_output, "Should return empty list when director not present")

    def test_fetch_director_multiple_directors(self):
        """ """
        input_str = '[{"name": "Director1", "job": "Director"}, {"name": "Director2", "job": "Director"}]'
        expected_output = ["Director1"]   
        result = fetch_director(input_str)
        self.assertEqual(result, expected_output, "Should return the first director found")

    @patch('preprocesser.pd.read_csv')
    @patch('preprocesser.storage')
    @patch('preprocesser.Movie')
    @patch('preprocesser.Credit')
    def test_load_csv_movies_csv(self, mock_credit, mock_movie, mock_storage, mock_read_csv):
        csv_path = "data_movies.csv"
        mock_read_csv.return_value = pd.DataFrame({
            'id': [1, 2],
            'title': ['Movie1', 'Movie2'],
            'budget': [1000000, 2000000],
            'homepage': ['http://movie1.com', 'http://movie2.com'],
            'original_language': ['en', 'en'],
            'original_title': ['Movie1 Original', 'Movie2 Original'],
            'overview': ['Overview1', 'Overview2'],
            'popularity': [7.5, 8.0],
            'release_date': ['2020-01-01', '2021-01-01'],
            'revenue': [5000000, 10000000],
            'runtime': [120, 130],
            'status': ['Released', 'Released'],
            'tagline': ['Tagline1', 'Tagline2'],
            'vote_average': [7.0, 8.0],
            'vote_count': [1500, 2500],
            'genres': ['[{"id":28,"name":"Action"}]', '[{"id":12,"name":"Adventure"}]'],
            'keywords': ['[{"id":609,"name":"hero"}]', '[{"id":121,"name":"journey"}]'],
            'production_countries': ['[{"iso_3166_1":"US","name":"United States of America"}]',
                                      '[{"iso_3166_1":"US","name":"United States of America"}]'],
            'production_companies': ['[{"id":1,"name":"Company1"}]', '[{"id":2,"name":"Company2"}]'],
            'spoken_languages': ['[{"iso_639_1":"en","name":"English"}]',
                                 '[{"iso_639_1":"en","name":"English"}]']
        })
        mock_storage.get_item_by_id.side_effect = [False, False]   

        load_csv(csv_path)

        self.assertEqual(mock_movie.call_count, 2, "Should create two Movie instances")
        self.assertEqual(mock_storage.get_item_by_id.call_count, 2, "Should check for duplicates twice")
        mock_movie.assert_any_call(
            movie_id=1,
            title='Movie1',
            budget=1000000,
            homepage='http://movie1.com',
            original_language='en',
            original_title='Movie1 Original',
            overview='Overview1',
            popularity=7.5,
            release_date=pd.to_datetime('2020-01-01'),
            revenue=5000000,
            runtime=120,
            status='Released',
            tagline='Tagline1',
            vote_average=7.0,
            vote_count=1500,
            genres='[{"id":28,"name":"Action"}]',
            keywords='[{"id":609,"name":"hero"}]',
            production_countries='[{"iso_3166_1":"US","name":"United States of America"}]',
            production_companies='[{"id":1,"name":"Company1"}]',
            spoken_languages='[{"iso_639_1":"en","name":"English"}]'
        )
        self.assertEqual(mock_credit.call_count, 0, "Should not process credits when loading movies.csv")

    @patch('preprocesser.pd.read_csv')
    @patch('preprocesser.storage')
    @patch('preprocesser.Movie')
    @patch('preprocesser.Credit')
    def test_load_csv_credits_csv(self, mock_credit, mock_movie, mock_storage, mock_read_csv):
        """ """
        csv_path = "data_credits.csv"
        mock_read_csv.return_value = pd.DataFrame({
            'movie_id': [1, 2],
            'title': ['Movie1', 'Movie2'],
            'cast': ['[{"name": "Actor1"}]', '[{"name": "Actor2"}]'],
            'crew': ['[{"name": "Director1", "job": "Director"}]', '[{"name": "Director2", "job": "Director"}]']
        })
         
        mock_storage.get_item_by_id.side_effect = [False, True, False, False]

        load_csv(csv_path)

        self.assertEqual(mock_credit.call_count, 1, "Should create one Credit instance")
        mock_credit.assert_called_with(
            movie_id=1,
            title='Movie1',
            cast='[{"name": "Actor1"}]',
            crew='[{"name": "Director1", "job": "Director"}]'
        )
        mock_movie.assert_not_called()

    @patch('preprocesser.pd.read_csv')
    def test_load_csv_invalid_file_type(self, mock_read_csv):
        """ """
        csv_path = "data_unknown.csv"
        with patch('builtins.print') as mock_print:
            load_csv(csv_path)
            mock_read_csv.assert_called_with(csv_path)
            mock_print.assert_any_call("Unsupported file type. Please provide either 'movies.csv' or 'credits.csv'.")

    @patch('preprocesser.pd.read_csv')
    def test_load_csv_no_csv_path(self, mock_read_csv):
        """ """
        with patch('builtins.print') as mock_print:
            load_csv(None)
            mock_read_csv.assert_not_called()
            mock_print.assert_any_call("Enter valid file path")

    @patch('preprocesser.storage')
    @patch('preprocesser.MovieContentBased')
    def test_save_processed_data(self, mock_movie_content_based, mock_storage):
        """ """
        movies_df = pd.DataFrame({
            'movie_id': [1, 2],
            'title': ['Movie1', 'Movie2'],
            'genres': [['Action'], ['Adventure']],
            'keywords': [['hero'], ['journey']],
            'cast': [['Actor1'], ['Actor2']],
            'director': [['Director1'], ['Director2']],
            'overview': ['Overview1', 'Overview2']
        })
        mock_storage.get_item_by_id.side_effect = [False, True]
        save_processed_data(movies_df)
        self.assertEqual(mock_movie_content_based.call_count, 1, "Should create one MovieContentBased instance")
        mock_movie_content_based.assert_called_with(
            movie_id=1,
            title='Movie1',
            genres=['Action'],
            keywords=['hero'],
            cast=['Actor1'],
            director=['Director1'],
            overview='Overview1'
        )
        self.assertEqual(mock_storage.get_item_by_id.call_count, 2, "Should check existence for two movies")
         
        instance = mock_movie_content_based.return_value
        instance.save.assert_called_once()

    @patch('preprocesser.storage')
    def test_load_processed_data(self, mock_storage):
        """ """
        mock_movie = MagicMock()
        mock_movie.to_dict.return_value = {
            'movie_id': 1,
            'title': 'Movie1',
            'genres': ['Action'],
            'keywords': ['hero'],
            'cast': ['Actor1'],
            'director': ['Director1'],
            'overview': 'Overview1'
        }
        mock_storage.all.return_value = [mock_movie]
        result = load_processed_data()
        expected_df = pd.DataFrame([{
            'movie_id': 1,
            'title': 'Movie1',
            'genres': ['Action'],
            'keywords': ['hero'],
            'cast': ['Actor1'],
            'director': ['Director1'],
            'overview': 'Overview1'
        }])
        pd.testing.assert_frame_equal(result, expected_df, check_dtype=False)

    @patch('preprocesser.save_processed_data')
    @patch('preprocesser.load_csv')
    @patch('preprocesser.load_processed_data')
    @patch('preprocesser.storage')
    def test_process_data_existing_data(self, mock_storage, mock_load_processed_data, mock_load_csv, mock_save_processed_data):
        """ """
        mock_load_processed_data.return_value = pd.DataFrame({
            'movie_id': [1],
            'title': ['Movie1'],
            'overview': ['Overview1'],
            'genres': [['Action']],
            'cast': [['Actor1']],
            'keywords': [['hero']],
            'crew': [['Director1']]
        })
        result = process_data()
        mock_load_processed_data.assert_called_once()
        mock_load_csv.assert_not_called()
        mock_save_processed_data.assert_not_called()
        self.assertIsInstance(result, pd.DataFrame, "Result should be a DataFrame")
        self.assertEqual(len(result), 1, "DataFrame should contain one movie")

    @patch('preprocesser.save_processed_data')
    @patch('preprocesser.load_csv')
    @patch('preprocesser.load_processed_data')
    @patch('preprocesser.storage')
    def test_process_data_empty_database(self, mock_storage, mock_load_processed_data, mock_load_csv, mock_save_processed_data):
        """ """
        mock_load_processed_data.return_value = pd.DataFrame()
        mock_storage.all.side_effect = [
            [],   
            []    
        ]

        with patch('builtins.print') as mock_print:
            result = process_data()
        mock_load_processed_data.assert_called_once()
        self.assertEqual(mock_load_csv.call_count, 2, "Should load both movies.csv and credits.csv")
        mock_save_processed_data.assert_called_once()
        self.assertIsInstance(result, pd.DataFrame, "Result should be a DataFrame")
         
        mock_print.assert_any_call("Merged columns:", pd.Index(['movie_id', 'title', 'overview', 'genres', 'cast', 'keywords', 'crew'], dtype='object'))

    @patch('preprocesser.save_processed_data')
    @patch('preprocesser.load_csv')
    @patch('preprocesser.load_processed_data')
    @patch('preprocesser.storage')
    def test_process_data_movie_not_found(self, mock_storage, mock_load_processed_data, mock_load_csv, mock_save_processed_data):
        """ """
        mock_load_processed_data.return_value = pd.DataFrame({
            'movie_id': [1],
            'title': ['Movie1'],
            'overview': ['Overview1'],
            'genres': [['Action']],
            'cast': [['Actor1']],
            'keywords': [['hero']],
            'crew': [['Director1']]
        })

        with self.assertRaises(IndexError) as context:
            process_data(movie_to_be_searched="Nonexistent Movie")
        self.assertEqual(str(context.exception), "Movie not found in the database.")

    @patch('preprocesser.save_processed_data')
    @patch('preprocesser.load_csv')
    @patch('preprocesser.load_processed_data')
    @patch('preprocesser.storage')
    def test_process_data_loading_error(self, mock_storage, mock_load_processed_data, mock_load_csv, mock_save_processed_data):
        """ """
        mock_load_processed_data.return_value = pd.DataFrame()
        mock_storage.all.side_effect = [
            [],   
            Exception("Failed to load movies")   
        ]

        with patch('builtins.print') as mock_print:
            result = process_data()

        mock_print.assert_any_call("Error loading movies data: Failed to load movies")

    @patch('preprocesser.pd.read_csv', side_effect=Exception("CSV read error"))
    def test_load_csv_exception_handling(self, mock_read_csv):
        """ """
        csv_path = "data_movies.csv"
         
        with patch('builtins.print') as mock_print:
            load_csv(csv_path)
            mock_print.assert_any_call("Error loading CSV: CSV read error")

    def test_fetch_director_no_director(self):
        """ """
        input_str = '[{"name": "Producer1", "job": "Producer"}]'
        expected_output = []
        result = fetch_director(input_str)
        self.assertEqual(result, expected_output, "Should return empty list when no director is present")

    @patch('preprocesser.pd.read_csv')
    @patch('preprocesser.storage')
    @patch('preprocesser.Movie')
    @patch('preprocesser.Credit')
    def test_load_csv_print_head(self, mock_credit, mock_movie, mock_storage, mock_read_csv):
        """ """
        csv_path = "data_movies.csv"
        df = pd.DataFrame({
            'id': [1, 2],
            'title': ['Movie1', 'Movie2'],
            'budget': [1000000, 2000000],
            'homepage': ['http://movie1.com', 'http://movie2.com'],
            'original_language': ['en', 'en'],
            'original_title': ['Movie1 Original', 'Movie2 Original'],
            'overview': ['Overview1', 'Overview2'],
            'popularity': [7.5, 8.0],
            'release_date': ['2020-01-01', '2021-01-01'],
            'revenue': [5000000, 10000000],
            'runtime': [120, 130],
            'status': ['Released', 'Released'],
            'tagline': ['Tagline1', 'Tagline2'],
            'vote_average': [7.0, 8.0],
            'vote_count': [1500, 2500],
            'genres': ['[{"id":28,"name":"Action"}]', '[{"id":12,"name":"Adventure"}]'],
            'keywords': ['[{"id":609,"name":"hero"}]', '[{"id":121,"name":"journey"}]'],
            'production_countries': ['[{"iso_3166_1":"US","name":"United States of America"}]',
                                      '[{"iso_3166_1":"US","name":"United States of America"}]'],
            'production_companies': ['[{"id":1,"name":"Company1"}]', '[{"id":2,"name":"Company2"}]'],
            'spoken_languages': ['[{"iso_639_1":"en","name":"English"}]',
                                 '[{"iso_639_1":"en","name":"English"}]']
        })
        mock_read_csv.return_value = df
        mock_storage.get_item_by_id.return_value = False

        with patch('builtins.print') as mock_print:
            load_csv(csv_path)
            mock_print.assert_any_call(['data', 'movies.csv'])
            mock_print.assert_any_call(df.head(5))

if __name__ == '__main__':
    unittest.main()

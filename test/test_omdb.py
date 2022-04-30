import logging
import unittest
from unittest.mock import patch
from requests.exceptions import ConnectionError
from src.settings import OMDB_API_KEY
from src.tools import omdb


@patch('src.tools.omdb.settings.OMDB_API_KEY', 'secret')
@patch('src.tools.omdb.logger')
@patch('src.tools.omdb.requests')
class TestGetOmdbData(unittest.TestCase):
    def test_get_omdb_data(self, mock_requests, _):
        mock_requests.get.return_value.json.return_value = {
            'Response': 'True'
        }
        result = omdb.get_omdb_data('Videodrome', 1983)
        self.assertEqual(result, {'Response': 'True'})
        mock_requests.get.assert_called_with(
            'http://www.omdbapi.com',
            params={
                'apiKey': 'secret',
                't': 'Videodrome',
                'y': 1983
            }
        )

    def test_get_omdb_data_not_found_results_in_info_log_message(self, mock_requests, mock_logger):
        mock_requests.get.return_value.json.return_value = {
            'Response': 'False',
            'Error': 'Movie not found!'
        }
        result = omdb.get_omdb_data('Videodrome', 1983)
        self.assertIsNone(result)
        mock_requests.get.assert_called_with(
            'http://www.omdbapi.com',
            params={
                'apiKey': 'secret',
                't': 'Videodrome',
                'y': 1983
            }
        )
        mock_logger.log.assert_called_once_with(
            logging.INFO,
            'Movie not found!'
        )

    def test_get_omdb_data_other_error_results_in_error_log_message(self, mock_requests, mock_logger):
        mock_requests.get.return_value.json.return_value = {
            'Response': 'False',
            'Error': 'Drat!'
        }
        result = omdb.get_omdb_data('Videodrome', 1983)
        self.assertIsNone(result)
        mock_requests.get.assert_called_with(
            'http://www.omdbapi.com',
            params={
                'apiKey': 'secret',
                't': 'Videodrome',
                'y': 1983
            }
        )
        mock_logger.log.assert_called_once_with(
            logging.ERROR,
            'Drat!'
        )

    def test_requests_exception_logged_and_swallowed(self, mock_requests, mock_logger):
        mock_requests.get.side_effect = ConnectionError()
        result = omdb.get_omdb_data('Videodrome', 1983)
        self.assertIsNone(result)
        mock_logger.error.assert_called_once()

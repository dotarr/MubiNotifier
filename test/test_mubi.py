import unittest
from copy import deepcopy
from unittest.mock import patch
from src.tools import mubi


@patch('src.tools.mubi._fetch_mubi_data')
class TestGetFeatured(unittest.TestCase):
    def setUp(self):
        self.mock_response = {
            'props': {
                'initialState': {
                    'filmProgramming': {
                        'filmProgrammings': [
                            {
                                'availability_object': 'blah_availability',
                                'filmId': 1234
                            }
                        ]
                    },
                    'film': {
                        'films': {
                            '1234': {
                                'film_metadata': 'blah_metadata'
                            }
                        }
                    }
                }
            }
        }

    def test_get_featured(self, mock_fetch):
        mock_fetch.return_value = self.mock_response
        response = mubi.get_featured()
        self.assertEqual(
            response,
            {
                'availability': {'availability_object': 'blah_availability', 'filmId': 1234},
                'film': {'film_metadata': 'blah_metadata'}
            }
        )


@patch('src.tools.mubi.json')
@patch('src.tools.mubi.BeautifulSoup')
@patch('src.tools.mubi.requests')
class TestFetchMubiData(unittest.TestCase):
    def test_fetch_mubi_data(self, mock_requests, mock_bs, mock_json):
        mock_requests.get.return_value.content = '<html>blah</html>'
        mock_bs.return_value.find.return_value.text = '{"blah":"blah"}'
        mock_json.loads.return_value = {'blah': 'blah'}

        result = mubi._fetch_mubi_data()

        mock_requests.get.assert_called_once_with(
            'https://mubi.com/film-of-the-day'
        )
        mock_bs.assert_called_once_with('<html>blah</html>', 'html.parser')
        mock_bs.return_value.find.assert_called_once_with(
            'script',
            {'id': '__NEXT_DATA__'}
        )
        mock_json.loads.assert_called_once_with('{"blah":"blah"}')
        self.assertEqual(result, {'blah': 'blah'})

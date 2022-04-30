import unittest
from unittest.mock import patch
from datetime import datetime
from src.tools import tweet_factory
import pytz
from freezegun import freeze_time


@patch('src.tools.tweet_factory._is_expiring')
@patch('src.tools.tweet_factory._get_ratings_str')
class TestComposeTweet(unittest.TestCase):
    def setUp(self):
        self.mubi_data = {
            'film': {
                'title': 'Trouble Every Day',
                'short_synopsis': 'mubi stuff happens'
            },
            'availability': {
                'availability_ends_at': '2022-02-15T00:00:00Z'
            }
        }
        self.omdb_data = {
            'Plot': 'omdb stuff happens'
        }

    def test_compose_omdb_found(self, mock_get_ratings, mock_expiring):
        mock_expiring.return_value = True
        mock_get_ratings.return_value = '[MC 9 | RT 97%]'
        response = tweet_factory.compose_tweet(self.mubi_data, self.omdb_data)
        self.assertEqual(
            response,
            "The film leaving #Mubi tonight is Trouble Every Day\n[MC 9 | RT 97%]\nomdb stuff happens"
        )

    def test_compose_omdb_not_found(self, mock_get_ratings, mock_expiring):
        mock_expiring.return_value = True
        mock_get_ratings.return_value = '[MC 9 | RT 97%]'
        response = tweet_factory.compose_tweet(self.mubi_data, None)
        self.assertEqual(
            response,
            "The film leaving #Mubi tonight is Trouble Every Day\n[MC 9 | RT 97%]\nmubi stuff happens"
        )

    def test_truncation(self, mock_get_ratings, mock_expiring):
        mock_expiring.return_value = True
        mock_get_ratings.return_value = ''
        self.mubi_data['film']['short_synopsis'] = "55 characters used up before the description which should give me 225 characters to play with, which is longer than you think when you're making stuff up as you go along. No really it is, nearly there now, not long, only a few words left"
        response = tweet_factory.compose_tweet(self.mubi_data, None)
        self.assertEqual(
            response,
            "The film leaving #Mubi tonight is Trouble Every Day\n\n55 characters used up before the description which should give me 225 characters to play with, which is longer than you think when you're making stuff up as you go along. No really it is, nearly there now, not long, only a f..."
        )
        self.assertEqual(len(response), 280)

    def test_featured_message_if_not_expiring(self, mock_get_ratings, mock_expiring):
        mock_expiring.return_value = False
        mock_get_ratings.return_value = '[MC 9 | RT 97%]'
        response = tweet_factory.compose_tweet(self.mubi_data, self.omdb_data)
        self.assertEqual(
            response,
            "Today\'s featured film on #Mubi is Trouble Every Day\n[MC 9 | RT 97%]\nomdb stuff happens"
        )


class TestGetRatingsStr(unittest.TestCase):
    def setUp(self):
        self.mubi_data = {
            'film': {
                'average_rating': 4.2
            }
        }
        self.omdb_data = {
            'Ratings':  [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.9/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "97%"
                }
            ]
        }

    def test_get_ratings_omdb_ratings_present(self):
        result = tweet_factory._get_ratings_str(self.mubi_data, self.omdb_data)
        self.assertEqual(
            result,
            '[IMDB: 7.9/10 | RT: 97%]'
        )

    def test_get_ratings_default_to_mubi_when_no_omdb_result(self):
        result = tweet_factory._get_ratings_str(self.mubi_data, None)
        self.assertEqual(
            result,
            '[Avg: 4.2]'
        )

    def test_ratings_not_in_source_map_still_appear(self):
        omdb_data = {
            'Ratings':  [
                {
                    "Source": "New Agg",
                    "Value": "7.9/10"
                }
            ]
        }
        result = tweet_factory._get_ratings_str(self.mubi_data, omdb_data)
        self.assertEqual(
            result,
            '[New Agg: 7.9/10]'
        )

    def test_omdb_data_present_but_no_ratings_section_empty(self):
        omdb_data = {
            'Ratings': []
        }
        result = tweet_factory._get_ratings_str(self.mubi_data, omdb_data)
        self.assertEqual(
            result,
            '[Avg: 4.2]'
        )

    def test_omdb_data_present_but_no_ratings_section_null(self):
        omdb_data = {
            'Ratings': None
        }
        result = tweet_factory._get_ratings_str(self.mubi_data, omdb_data)
        self.assertEqual(
            result,
            '[Avg: 4.2]'
        )

    def test_omdb_data_present_but_no_ratings_section_missing(self):
        omdb_data = {
            'another_field': 'blah'
        }
        result = tweet_factory._get_ratings_str(self.mubi_data, omdb_data)
        self.assertEqual(
            result,
            '[Avg: 4.2]'
        )


class TestIsExpiring(unittest.TestCase):
    @freeze_time("2022-01-14 14:21:34")
    def test_is_expiring(self):
        self.assertTrue(tweet_factory._is_expiring('2022-01-15T00:00:00Z'))

    @freeze_time("2022-05-14 14:21:34")
    def test_is_expiring_dst(self):
        self.assertTrue(tweet_factory._is_expiring('2022-05-14T23:00:00Z'))

    @freeze_time("2022-05-14 14:21:34")
    def test_is_not_expiring(self):
        self.assertFalse(tweet_factory._is_expiring('2022-02-15T00:00:00Z'))

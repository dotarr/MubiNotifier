from unittest.mock import patch, call
from copy import deepcopy
import unittest
import os

os.environ.update(
    {
        'twitter_consumer_key': 'key',
        'twitter_consumer_secret': 'secret',
        'twitter_access_token_key': 'token_key',
        'twitter_access_token_secret': 'token_secret',
        'omdb_api_key': 'secret'
    }
)

from src import mubi_notifier

@patch('src.mubi_notifier.twitter.Api')
@patch('src.mubi_notifier.tweet_factory')
@patch('src.mubi_notifier.omdb')
@patch('src.mubi_notifier.mubi')
class TestSendNotification(unittest.TestCase):
    def setUp(self):
        self.mock_mubi_data = {
            'film': {
                'title': 'The Big Sleep',
                'original_title': 'peelS giB ehT',
                'year': 1946,
                'stills': {'medium': 'https://example.com/img.png'}
            },
            'availability': {}
        }

        self.mock_omdb_data = {
            "Title": "The Big Sleep",
            "Year": "1946",
            "Plot": "Private detective Philip Marlowe is hired by a wealthy family. Before the complex case is over, he's seen murder, blackmail, and what might be love.",
            "Ratings": [
                {
                    "Source": "Internet Movie Database",
                    "Value": "7.9/10"
                },
                {
                    "Source": "Rotten Tomatoes",
                    "Value": "97%"
                }
            ],
            "Response": "True"
        }

    def test_send_notification(
        self,
        mock_mubi,
        mock_omdb,
        mock_tweet_factory,
        mock_twitter,
    ):
        mock_mubi.get_featured.return_value = self.mock_mubi_data
        mock_omdb.get_omdb_data.return_value = self.mock_omdb_data
        mock_tweet_factory.compose_tweet.return_value = 'this is a tweet'

        mubi_notifier.send_notification({}, {})
        mock_mubi.get_featured.assert_called_once()
        mock_omdb.get_omdb_data.assert_called_once_with('The Big Sleep', 1946)

        mock_tweet_factory.compose_tweet.assert_called_once_with(
            self.mock_mubi_data,
            self.mock_omdb_data
        )
        mock_twitter.assert_called_with(
            consumer_key='key',
            consumer_secret='secret',
            access_token_key='token_key',
            access_token_secret='token_secret'
        )
        mock_twitter.return_value.PostUpdate.assert_called_once_with(
            'this is a tweet',
            media='https://example.com/img.png'
        )

    def test_send_notification_original_title_used_if_title_gets_no_omdb_results(
        self,
        mock_mubi,
        mock_omdb,
        mock_tweet_factory,
        mock_twitter,
    ):
        mock_mubi.get_featured.return_value = self.mock_mubi_data
        mock_omdb.get_omdb_data.side_effect = [None, self.mock_omdb_data]
        mock_tweet_factory.compose_tweet.return_value = 'this is a tweet'

        mubi_notifier.send_notification({}, {})
        mock_mubi.get_featured.assert_called_once()
        mock_omdb.get_omdb_data.assert_has_calls(
            [call(_, 1946) for _ in ['The Big Sleep', 'peelS giB ehT']],
            any_order=False
        )
        mock_tweet_factory.compose_tweet.assert_called_once_with(
            self.mock_mubi_data,
            self.mock_omdb_data
        )
        mock_twitter.assert_called_with(
            consumer_key='key',
            consumer_secret='secret',
            access_token_key='token_key',
            access_token_secret='token_secret'
        )
        mock_twitter.return_value.PostUpdate.assert_called_once_with(
            'this is a tweet',
            media='https://example.com/img.png'
        )

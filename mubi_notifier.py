"""
A lambda to tweet out information about titles joining/leaving mubi
"""

import logging
import os

from lib.mubi import MubiUtil
from lib.omdb import OmdbUtil
from lib.tweet_factory import TweetFactory
from lib.twitter_util import TwitterUtil

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_config():
    """Pulls config from environment variables"""
    config = {
        'mubi_country_code' : os.environ['mubi_country_code'],
        'omdb_api_key' : os.environ['omdb_api_key'],
        'twitter_consumer_key' : os.environ['twitter_consumer_key'],
        'twitter_consumer_secret' : os.environ['twitter_consumer_secret'],
        'twitter_access_token_key' : os.environ['twitter_access_token_key'],
        'twitter_access_token_secret' :os.environ['twitter_access_token_secret']
    }
    return config

def send_notification(event, context):
    """
    Main controller. Fetches mubi/omdb data, generates a message and
    tweets it out.
    """
    logging.info('%s %s', event, context)
    config = get_config()

    mubi = MubiUtil(config)
    omdb = OmdbUtil(config)
    twitter = TwitterUtil(config)

    logging.info('fetching mubi json')
    film_json = mubi.get_film_json()
    logger.info('fetched %s titles', (len(film_json)))

    leaving = mubi.get_leaving(film_json)
    logger.info('film leaving is %s', leaving['title'])

    logger.info('getting omdb data')
    omdb_json = omdb.get_omdb_data(leaving['title'], leaving['year'])
    logger.info('fetched omdb data %s', omdb_json)

    msg = TweetFactory.compose_tweet(leaving, omdb_json)
    logger.info('sending tweet - %s', msg)
    twitter.send_tweet(msg, leaving['stills']['medium'])

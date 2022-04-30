import logging

import twitter

from tools import mubi, omdb, tweet_factory
from settings import TWITTER_CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def send_notification(event: dict, context: dict):
    """
    Main controller. Fetches Mubi/OMDB data, generates a message and
    tweets it out.

    :param event: AWS event dict - not processed
    :type event: dict
    :param context: AWS context dict - not processed
    :type context: dict
    """

    mubi_data = mubi.get_featured()

    logger.info('film leaving is %s', mubi_data['film']['title'])

    for t in ['title', 'original_title']:
        if (omdb_data := omdb.get_omdb_data(
                mubi_data['film'][t], mubi_data['film']['year'])):
            break

    logger.info('fetched omdb data %s', omdb_data)

    msg = tweet_factory.compose_tweet(mubi_data, omdb_data)
    logger.info('sending tweet - %s', msg)

    twitter.Api(**TWITTER_CONFIG).PostUpdate(
        msg,
        media=mubi_data['film']['stills']['medium']
    )

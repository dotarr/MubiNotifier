"""
A proxy module for the python twitter libraries
"""
import logging

import twitter

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class TwitterUtil:
    """Proxy twitter class"""
    def __init__(self, config):
        self._api = twitter.Api(consumer_key=config['twitter_consumer_key'],
                                consumer_secret=config['twitter_consumer_secret'],
                                access_token_key=config['twitter_access_token_key'],
                                access_token_secret=config['twitter_access_token_secret'])

    def send_tweet(self, msg, img_url):
        """Sends the tweet including image"""
        try:
            result = self._api.PostUpdate(msg,
                                          media=img_url)
            logger.info(result)
        except Exception as exception:
            logger.error('Exception when trying to send tweet %s',
                         exception)
            raise RuntimeError('Error Sending Tweet')

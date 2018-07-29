"""
A module to handle requests to the OMDB API
"""
import logging
from urllib.parse import quote
#pip
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BASE_URL = 'http://www.omdbapi.com/?apikey={}'
TITLE_QUERY = '&t={}'

class OmdbUtil:
    """ A class that handles calls to the OMDB api """
    def __init__(self, config):
        self._api_url = BASE_URL.format(config['omdb_api_key'])

    def _fetch_raw_film_data(self, title):
        request = '{}{}'.format(self._api_url, TITLE_QUERY.format(quote(title)))
        try:
            response = requests.get(request)
        except requests.exceptions.RequestException as exception:
            logger.info('Exception thrown by requests %s', exception)
            raise RuntimeError('Requests exception')

        if response.status_code != 200:
            logger.error('Recieved http %s response. \n %s',
                         response.status_code,
                         response.text)

            raise RuntimeError('Bad Response from OMDB')

        return response

    def get_omdb_data(self, title):
        """ Fetches data from omdb based on title """
        try:
            response = self._fetch_raw_film_data(title)
        except RuntimeError as exception:
            logger.error('Exception thrown when trying to get omdb data %s',
                         exception)
            return None
        omdb_json = response.json()

        if not response:
            return None
        if omdb_json['Response'] == 'False':
            if 'Error' in omdb_json:
                if omdb_json['Error'] == 'Movie not found!':
                    logger.info('Couldn\'t find %s', title)
                    return None
                logger.error('Error response from omdb: %s', omdb_json)
                return None
            logger.warning('Response element is false, but no error: %s',
                           omdb_json['Response'])
            return None
        return omdb_json

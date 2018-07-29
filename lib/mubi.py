"""
A module to handle requests to the MUBI API
"""
import datetime
import logging
import requests

#pip imports
from dateutil.parser import parse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BASE_URL = 'https://mubi.com/services/android/films?country={}'

class MubiUtil:
    """A class that handles calls to the Mubi api"""
    def __init__(self, config):
        self._api_url = BASE_URL.format(config['mubi_country_code'])

    def _fetch_raw_film_listings(self):
        response = requests.get(self._api_url)

        if response.status_code != 200:
            logger.error('Recieved http %s response. \n %s',
                         response.status_code,
                         response.text)

            raise Exception('Bad Response from Mubi')
        return response

    def get_film_json(self):
        """ returns all film data as json"""
        raw_response = self._fetch_raw_film_listings()
        return raw_response.json()
    @staticmethod
    def get_leaving(film_json):
        """ returns the film leaving mubi today based on current date"""
        today = datetime.date.today()
        for film in reversed(film_json):
            if parse(film['expires_at']).date() == today:
                return film
        return None

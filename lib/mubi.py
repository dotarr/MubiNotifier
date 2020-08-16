"""
A module to handle requests to the MUBI API
"""
import json
import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BASE_URL = 'https://mubi.com/film-of-the-day'


class MubiUtil:
    """A class that handles calls to the Mubi api"""

    def _fetch_mubi_data(self):
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        raw_data = soup.find('script', {'id': '__NEXT_DATA__'}).text
        data = json.loads(raw_data)
        return data

    def get_leaving(self):
        """ returns the film leaving mubi today based on current date"""
        data = self._fetch_mubi_data()['props']['initialState']
        leaving_film_data = data['filmProgramming']['filmProgrammings'][0]
        film_list = data['film']['films']
        return {
            'availability' : leaving_film_data,
            'film': film_list[str(leaving_film_data['filmId'])]
        }

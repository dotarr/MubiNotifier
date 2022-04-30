import json

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://mubi.com/film-of-the-day'


def get_featured() -> dict:
    """
    Fetches availability and metadata on the currently featured film in the form:


    :return: the information of the current film in the format:
        {
            'availability': availability information,
            'film' : metadata (title, description, rating...)
        }
    :rtype: dict
    """
    data = _fetch_mubi_data()['props']['initialState']
    leaving_film_data = data['filmProgramming']['filmProgrammings'][0]
    film_list = data['film']['films']
    return {
        'availability': leaving_film_data,
        'film': film_list[str(leaving_film_data['filmId'])]
    }


def _fetch_mubi_data() -> dict:
    """
    Fetches raw JSON data embedded in the __NEXT_DATA__ section of the Mubi
    now showing film of the day page

    :return: the JSON data 
    :rtype: dict
    """
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    raw_data = soup.find('script', {'id': '__NEXT_DATA__'}).text
    return json.loads(raw_data)

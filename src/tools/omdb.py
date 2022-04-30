import logging
from typing import Optional
from urllib.parse import quote

import requests
import settings

logger = logging.getLogger(__name__)

OMDB_URL = 'http://www.omdbapi.com'


def get_omdb_data(title: str, year: int) -> Optional[dict]:
    """
    Fetches film information from OMDB based on the title and the year of release

    Requests exceptions are logged and swallowed since we can fall back to OMDB
    data

    :param title: The title of the film to be searched
    :type title: str
    :param year: The year of release
    :type year: int
    :return: The OMDB information on this film or None
    :rtype: Optional[dict]
    """
    params = {
        'apiKey': settings.OMDB_API_KEY,
        't': title,
        'y': year
    }

    try:
        response = requests.get(OMDB_URL, params=params)
        omdb_json = response.json()
    except Exception as e:
        logger.error(e)
        return

    if omdb_json['Response'] == 'True':
        return omdb_json

    logger.log(
        logging.ERROR if omdb_json.get('Error') != 'Movie not found!' else logging.INFO,
        omdb_json.get('Error', omdb_json)
    )

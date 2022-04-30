import datetime
from typing import Optional

import dateutil.parser
import pytz
from settings import TIMEZONE

CHAR_LIMIT = 280

SCORE_MAPPINGS = {
    'Internet Movie Database': 'IMDB',
    'Rotten Tomatoes': 'RT',
    'Metacritic': 'MC'
}


def compose_tweet(mubi_data: dict, omdb_data: Optional[dict]) -> str:
    """
    Composes the message for the outgoing tweet containing the title, rating and
    plot description. If the message exceeds the 280 character limit, the
    message will be truncated with a trailing ellipsis. OMDB summary/ratings
    take precedence with Mubi data acting as a fallback

    :param mubi_data: the data fetched from Mubi
    :type mubi_data: dict
    :param omdb_data: the data fetched from OMDB
    :type omdb_data: Optional[dict]
    :return: the message to be tweeted
    :rtype: str
    """

    title_msg = {
        True: 'The film leaving #Mubi tonight is {}',
        False: 'Today\'s featured film on #Mubi is {}'
    }[_is_expiring(mubi_data['availability']['availability_ends_at'])]

    msg = '{title}\n{rating}\n{plot}'.format(
        title=title_msg.format(mubi_data['film']['title']),
        rating=_get_ratings_str(mubi_data, omdb_data),
        plot=omdb_data['Plot'] if omdb_data else mubi_data['film']['short_synopsis']
    )

    return msg[:CHAR_LIMIT - 3] + (msg[CHAR_LIMIT - 3:] and '...')


def _get_ratings_str(mubi_data: dict, omdb_data: Optional[dict]) -> str:
    """
    Helper function for compiling ratings section
    Returns a list in the format "[Source1 6.7 | Source2 2.2 | ...]"
    Attempts to use ratings fetched from OMDB (e.g. IMDB, Rotten Tomatoes ...)
    Falls-back to Mubi's average ratings

    :param mubi_json: the data fetched from Mubi
    :type mubi_json: dict
    :param omdb_json: _description_
    :type omdb_json: Optional[dict]
    :return: the data fetched from OMDB
    :rtype: str
    """

    if not (omdb_ratings := (omdb_data or {}).get('Ratings')):
        return '[Avg: {}]'.format(mubi_data['film']['average_rating'])

    ratings = [
        '{}: {}'.format(
            SCORE_MAPPINGS.get(r['Source'], r['Source']),
            r['Value']
        )
        for r in omdb_ratings
    ]

    return '[{}]'.format(' | '.join(ratings))


def _is_expiring(expiry: str) -> bool:
    """
    Helper function to determine if a film is expiring.
    Films expire at midnight local time, but expiry time is in UTC.
    Therefore 'midnight tomorrow' is converted to UTC for comparison.

    :param expiry: a string representing this film's expiry time
    :type expiry: str
    :return: True if this utc value matches the value of 'midnight tomorrow' in utc
    :rtype: bool
    """
    midnight_dt = (
        datetime.timedelta(days=1) +
        datetime.datetime.now(pytz.timezone(TIMEZONE))
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .astimezone(pytz.utc)
    )
    expiry_dt = dateutil.parser.isoparse(expiry)

    return midnight_dt == expiry_dt

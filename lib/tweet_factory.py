"""
A factory class for making the tweet
"""

TWITTER_CHAR_LIMIT = 280

SCORE_MAPPINGS = {'Internet Movie Database' : 'IMDB',
                  'Rotten Tomatoes' : 'RT',
                  'Metacritic' : 'MC'}

class TweetFactory:
    """Generates plain text tweet"""
    @staticmethod
    def compose_tweet(mubi_json, omdb_json):
        """Composes the tweet"""
        msgs = []
        msgs.append("The film leaving Mubi tonight is {}".format(
            mubi_json['title']))
        ratings = TweetFactory._get_ratings_str(mubi_json, omdb_json)
        if ratings:
            msgs.append(ratings)

        if omdb_json:
            msgs.append(omdb_json['Plot'])
        else:
            msgs.append(mubi_json['excerpt'])

        msg = '\n'.join(msgs)
        return msg[:TWITTER_CHAR_LIMIT - 3] +\
                (msg[TWITTER_CHAR_LIMIT - 3:] and '...')

    @staticmethod
    def _get_ratings_str(mubi_json, omdb_json):
        ratings = []
        if omdb_json and 'Ratings' in omdb_json:
            for rating in omdb_json['Ratings']:
                ratings.append('{}: {}'.format(SCORE_MAPPINGS[rating['Source']],
                                               rating['Value']))
        else:
            ratings.append('Average Rating: {}'
                           .format(mubi_json['average_rating']))
        return '[{}]'.format('|'.join(ratings)) if ratings else None

"""
A factory class for making the tweet
"""

TWITTER_CHAR_LIMIT = 280

SCORE_MAPPINGS = {'Internet Movie Database' : 'imdb',
                  'Rotten Tomatoes' : 'rt',
                  'Metacritic' : 'mc'}

class TweetFactory:
    """Generates plain text tweet"""
    @staticmethod
    def compose_tweet(mubi_json, omdb_json):
        """Composes the tweet"""
        msgs = []
        msgs.append("The film leaving Mubi tonight is {}".format(
            mubi_json['title']))

        if omdb_json:
            ratings = TweetFactory._get_ratings(omdb_json)
            msgs.append('[RT: {} | IMDB: {} | MC: {}]'.format(ratings['rt'],
                                                              ratings['imdb'],
                                                              ratings['mc']))
            msgs.append(omdb_json['Plot'])
        else:
            msgs.append('Average Rating: {}'
                        .format(mubi_json['average_rating']))
            msgs.append(mubi_json['excerpt'])
        msg = '\n'.join(msgs)
        return msg[:TWITTER_CHAR_LIMIT - 3] +\
                    (msg[TWITTER_CHAR_LIMIT - 3:] and '...')

    @staticmethod
    def _get_ratings(omdb_json):
        ratings = {}
        for rating in omdb_json['Ratings']:
            ratings[SCORE_MAPPINGS[rating['Source']]] = rating['Value']
        return ratings

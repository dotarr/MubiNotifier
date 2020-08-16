import os

TWITTER_CONFIG = {
    k: os.environ[f'twitter_{k}'] for k in [
        'consumer_key',
        'consumer_secret',
        'access_token_key',
        'access_token_secret'
    ]
}

OMDB_API_KEY = os.environ['omdb_api_key']

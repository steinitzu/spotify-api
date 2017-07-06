import os

import pytest

from spotify.auth import OAuth
from spotify.client import Client

CLIENT_ID = os.environ['SPOTAPI_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTAPI_CLIENT_SECRET']
REFRESH_TOKEN = os.environ['SPOTAPI_REFRESH_TOKEN']
FRANK_ZAPPA = '6ra4GIOgCZQZMOaUECftGN'


@pytest.fixture
def spotify_auth():
    auth = OAuth(CLIENT_ID, CLIENT_SECRET)
    return auth


@pytest.fixture
def ccspotify(spotify_auth):
    """
    Spotify client authorized with client credentials.
    """
    client = Client(spotify_auth)
    client.auth.request_client_credentials()
    print(client.auth.token)
    return client


def test_get_artist(ccspotify):
    frank = ccspotify.api.artist(FRANK_ZAPPA)
    assert frank['name'] == 'Frank Zappa'
    assert frank['type'] == 'artist'

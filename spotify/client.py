import requests
from functools import wraps

from .auth import OAuth
from . import endpoints


class Client:
    prefix = 'https://api.spotify.com/v1'

    api = endpoints  # So static analysis is useful

    def __init__(self, auth: OAuth, requests_session=None):
        self.session = requests_session or requests.Session()
        self.auth = auth

        class Api:
            pass
        self.api = Api()  # So endpoints module is not modified
        self.api.request = self.request

        for name, member in endpoints.__dict__.items():
            if name.startswith('_'):
                continue
            method = self._build_request(member)
            setattr(self.api, name, method)

    def _build_request(self, func):
        # Takes endpoint functions and performs actual requests
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.request(**func(*args, **kwargs))
        return wrapper
            
    def headers(self):
        return {'Authorization': 'Bearer '+self.auth.token['access_token']}

    def request(self, method, url, params=None, payload=None):
        url = url if url.startswith('http') else self.prefix+url
        headers = self.headers()
        response = self.session.request(
            method, url, params=params, json=payload, headers=headers
        )
        response.raise_for_status()
        if not response.text:
            return
        return response.json()

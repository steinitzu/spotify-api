import time
from urllib.parse import parse_qs, urlencode, urlsplit

import requests
from requests.auth import HTTPBasicAuth


class OAuth:
    AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, redirect_uri=None, scopes=(), state=None,
                 auto_refresh=None, requests=requests):
        """
        Handles OAuth authentication for the Spotify web API.
        Supports client credentials and user auth flows.
        
        Args:
            client_id(str): The spotify app client id
            client_secret(str): The Spotify app secret
            redirect_uri(str(url)): Redirect URI for this app (not needed for client credentials)
            scopes(list|space separated str): A list of user data scopes
                (see: https://developer.spotify.com/web-api/using-scopes/)
            state(str): Optional unique state value to verify requests
            auto_refresh(int): Optional, when set the token is auto refreshed
                as needed on access if it expires in less than the value given in seconds.
            requests_session(requests.Session() or compatible object), defaults to a new requests.Sesssion()
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        if isinstance(scopes, str):
            self.scopes = scopes
        else:
            self.scopes = ' '.join(scopes)
        self.state = state
        self._token = None
        self.auto_refresh = auto_refresh

        self.session = requests or requests.Session()

    @property
    def authorize_url(self):
        """
        Generated OAuth authorization URL that user can be redirected to.

        Returns:
            str (URL)
        """
        params = dict(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            response_type='code',
        )
        if self.scopes:
            params['scope'] = self.scopes
        if self.state:
            params['state'] = self.state
        params = urlencode(params)
        return '{}?{}'.format(self.AUTHORIZE_URL, params)

    @property
    def token(self):
        if self.auto_refresh:
            self.refresh_token_if_needed(self.auto_refresh)
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def parse_response_code(self, url):
        q = parse_qs(urlsplit(url).query)
        return q['code'][0]

    def request_token(self, url_or_code):
        """
        Requests an access token given a response code or url containing
        response code in a ?code query param.
        The token will be set to this instance's `token` attribute.

        Raises HTTPError on any non 2xx response code
        """
        if url_or_code.startswith('http'):
            code = self.parse_response_code(url_or_code)
        else:
            code = url_or_code

        params = {
            'redirect_uri': self.redirect_uri,
            'code': code,
            'grant_type': 'authorization_code'
        }
        if self.scopes:
            params['scope'] = self.scopes
        if self.state:
            params['state'] = self.state
        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        response = self.session.post(self.TOKEN_URL, data=params, auth=auth, verify=True)
        response.raise_for_status()
        token = response.json()
        token['expires_at'] = int(time.time()) + token['expires_in']
        self.token = token

    def request_client_credentials(self):
        """
        Fetches a client credentials token using the current app settings.
        resulting token will be saved in `self.token`

        Raises HTTPError on any non 2xx response code
        """
        params = {'grant_type': 'client_credentials'}
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        response = self.session.post(self.TOKEN_URL, data=params, auth=auth, verify=True)
        response.raise_for_status()
        token = response.json()
        token['expires_at'] = int(time.time()) + token['expires_in']
        self.token = token

    def refresh_token(self):
        """
        Refresh token regardless of when it expires.

        Raises HTTPError on any non 2xx response code
        """
        refresh_token = self._token['refresh_token']        
        params = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        response = self.session.post(self.TOKEN_URL, data=params, auth=auth)
        response.raise_for_status()
        token = response.json()
        token['expires_at'] = int(time.time()) + token['expires_in']
        if 'refresh_token' not in token:
            token['refresh_token'] = refresh_token
        self.token = token

    def refresh_token_if_needed(self, expires_in=300):
        """
        Refresh the current token if it expires in < `expires_in` seconds.

        Raises HTTPError on failed token refresh
        """
        if self._token['expires_at'] <= time.time() + expires_in:
            if 'refresh_token' in self._token:
                self.refresh_token()
            else:
                self.request_client_credentials()

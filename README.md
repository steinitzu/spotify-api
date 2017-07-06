# spotify-api
Python API client for the spotify web API.  
[https://developer.spotify.com/web-api/](https://developer.spotify.com/web-api/)

# Usage

## Intro

```python
from spotify import Client, OAuth

auth = OAuth('MY_CLIENT_ID', 'MY_CLIENT_SECRET')
auth.request_client_credentials()

client = Client(auth)

albums = client.api.search('artist:frank zappa', type='artist', 'album')
```

## Flask example with OAuth

```python
from flask import Flask, redirect, request, session, url_for, jsonify
from spotify import OAuth, Client


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

def get_auth(token=None):
    auth = OAuth(
        'MY_CLIENT_ID', 
        'MY_CLIENT_SECRET', 
        redirect_uri='http://my_redirect_uri',
        scopes=['user-read-private', 'user-top-read']
    )
    auth.token = token
    return auth
    
    
    
@app.route('/the_app')
def the_app():
    token = session.get('spotify_token')
    if not token:
        return redirect(url_for('authorize'))
    client = Client(get_auth(token))
    
    return jsonify([
        client.api.me(),
        client.api.me_top('artists')
    ])
    
    
@app.route('/authorize')
def authorize():
    auth = get_auth()
    return redirect(auth.authorize_url)
    
    
@app.route('/callback')  # redirect uri should point to this
def callback():
    auth = get_auth()
    auth.request_token(request.url)
    session['spotify_token'] = auth.token
    return redirect(url_for('the_app'))
```

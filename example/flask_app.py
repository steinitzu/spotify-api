import base64
from flask import Flask, redirect, request, session, url_for, jsonify
from spotify import OAuth, Client


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

def get_auth(token=None):
    auth = OAuth(
        'CLIENT_ID',  # Replace these with your client id and secret
        'CLIENT_SECRET',
        redirect_uri='http://127.0.0.1:5000/callback',
        scopes=["user-read-private", "user-top-read",
                "ugc-image-upload", "playlist-modify-public",
                "playlist-modify-private", ]
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


# For testing the new endpoint, might remove later
@app.route('/playlist')
def playlist():
    token = session.get('spotify_token')
    if not token:
        return redirect(url_for('authorize'))
    client = Client(get_auth(token))
    # Expects a file called "1.jpg" in example directory
    with open("1.jpg", "rb") as f:
        image = base64.b64encode(f.read())  # encode the image to base64

    return client.api.user_playlist_custom_cover("2vfGKaDXBH7ZSmGVXVeI5o", image)


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

"""
URL generation functions.

All functions return a tuple of `method (str), url (str), params (dict), payload (dict)`
in that order (`params` and `payload` are optional).
ex. ('GET', '/me/tracks', {'limit': 40})

All functions defined here are decorated to convert the return value to a dict with keys {method, url, params, payload}.
"""
from decorator import decorator as _deco
import sys as _sys
import inspect as _inspect


def album(id, market=None):
    return 'GET', '/albums/{}'.format(id), {'market': market}


def albums(ids, market=None):
    ids = ','.join(ids)
    return 'GET', '/albums', dict(ids=ids, market=market)


def album_tracks(id, limit=50, offset=0, market=None):
    return 'GET', '/albums/{}/tracks'.format(id), dict(limit=limit, offset=offset, market=market)


def artist(id):
    return 'GET', '/artists/{}'.format(id),


def artists(ids):
    ids = ','.join(ids)
    return 'GET', '/artists', {'ids': ids}


def artist_albums(id, album_type=None, market=None, limit=50, offset=0):
    return (
        'GET', '/artists/{}/albums'.format(id),
        dict(album_type=album_type, market=market, limit=limit, offset=offset)
    )


def track(id, market=None):
    return 'GET', '/tracks/{}'.format(id), {'market': market}


def track_audio_features(track_id):
    return 'GET', '/audio-features/{}'.format(track_id)


def tracks(ids, market=None):
    return 'GET', '/tracks', {'market': market, 'ids': ','.join(ids)}


def tracks_audio_features(track_ids):
    return 'GET', '/audio-features', dict(ids=','.join(track_ids))


def artist_top_tracks(id, country):
    return 'GET', '/artists/{}/top-tracks'.format(id), dict(country=country)


def artist_related_artists(id):
    return 'GET', '/artists/{}/related-artists'.format(id),


def browse_featured_playlists(locale=None, country=None, timestamp=None, limit=50, offset=0):
    return (
        'GET', '/browse/features-playlists',
        dict(locale=locale, country=country,
             timestamp=timestamp, limit=limit, offset=offset)
    )


def browse_new_releases(country=None, limit=50, offset=0):
    return (
        'GET', '/browse/new-releases',
        dict(country=country, limit=limit, offset=offset)
    )


def browse_categories(locale=None, country=None, limit=50, offset=0):
    return (
        'GET', '/browse/categories',
        dict(locale=locale, country=country, limit=limit, offset=offset)
    )


def browse_category(id, locale=None, country=None):
    return 'GET', '/browse/categories/{}'.format(id), dict(locale=locale, country=country)


def browse_category_playlists(id, country=None, limit=50, offset=0):
    return (
        'GET', '/browse/categories/{}/playlists'.format(id),
        dict(country=country, limit=limit, offset=offset)
    )


def recommendations(seed_artists=None, seed_tracks=None, seed_genres=None, market=None, limit=100, **tuneables):
    params = {'limit': limit}
    if seed_artists:
        params['seed_artists'] = ','.join(seed_artists)
    if seed_tracks:
        params['seed_tracks'] = ','.join(seed_tracks)
    if seed_genres:
        params['seed_genres'] = ','.join(seed_genres)
    if market:
        params['market'] = market
    params.update(tuneables)
    return 'GET', '/recommendations', params


def me():
    """
    Current user's profile
    """
    return 'GET', '/me'


def me_following(type='artist', limit=50, after=None):
    """
    Followed artists of current user.
    """
    return 'GET', '/me/following', dict(type=type, limit=limit, after=after)


def me_follow(type, ids):
    """
    Follow artists or users. Max 50 ids
    """
    return 'PUT', '/me/following', {'type': type}, {'ids': ids}


def me_unfollow(type, ids):
    return 'DELETE', '/me/following', {'type': type}, {'ids': ids}


def me_following_contains(type, ids):
    return 'GET', '/me/following/contains', {'type': type, 'ids': ids},


def me_follow_playlist(owner_id, playlist_id, public=True):
    return (
        'PUT', '/users/{}/playlists/{}/followers'.format(owner_id, playlist_id),
        {'public': public}
    )


def me_unfollow_playlist(owner_id, playlist_id):
    return 'DELETE', '/users/{}/playlists/{}/followers'.format(owner_id, playlist_id),


def users_following_contains_playlists(owner_id, playlist_id, user_ids):
    return (
        'GET', '/users/{}/playlists/{}/followers/contains'.format(
            owner_id, playlist_id),
        {'ids': ','.join(user_ids)}
    )


def me_tracks_add(ids):
    return 'PUT', '/me/tracks', {'ids': ','.join(ids)}


def me_tracks(limit=50, offset=0, market=None):
    return 'GET', '/me/tracks', dict(limit=limit, offset=offset, market=market)


def me_tracks_remove(ids):
    return 'DELETE', '/me/tracks', dict(ids=ids)


def me_tracks_contains(ids):
    return 'GET', '/me/tracks/contains', dict(ids=ids)


def me_albums_add(ids):
    return 'PUT', '/me/albums', {'ids': ','.join(ids)}


def me_albums(limit=50, offset=0, market=None):
    return 'GET', '/me/albums', dict(limit=limit, offset=offset, market=market)


def me_albums_remove(ids):
    return 'DELETE', '/me/albums', dict(ids=ids)


def me_albums_contains(ids):
    return 'GET', '/me/albums/contains', dict(ids=ids)


def me_top(type, limit=50, offset=0, time_range='medium_term'):
    return (
        'GET', '/me/top/{}'.format(type),
        dict(limit=limit, offset=offset, time_range=time_range)
    )

def me_player_recently_played(limit=50, before=None, after=None):
    return (
        'GET', '/me/player/recently-played',
        dict(limit=limit, before=before, after=after)
    )

# TODO: /player endpoints


def user_playlists(user_id, limit=50, offset=0):
    return 'GET', '/users/{}/playlists'.format(user_id), dict(limit=limit, offset=offset)


def me_playlists(limit=50, offset=0):
    return 'GET', '/me/playlists', dict(limit=limit, offset=offset)


def user_playlist(user_id, playlist_id, fields=None, market=None):
    return (
        'GET', '/users/{}/playlists/{}'.format(user_id, playlist_id),
        dict(fields=fields, market=market)
    )


def user_playlist_tracks(user_id, playlist_id, fields=None, limit=100, offset=0, market=None):
    return (
        'GET', '/users/{}/playlists/{}/tracks'.format(user_id, playlist_id),
        dict(fields=fields, limit=limit, offset=offset, market=market)
    )


def user_playlist_create(user_id, name, public=True, collaborative=False, description=None):
    return (
        'POST', '/users/{}/playlists'.format(user_id), {},
        dict(name=name, public=public,
             collaborative=collaborative, description=description)
    )


def user_playlist_tracks_add(user_id, playlist_id, track_uris, position=None):
    payload = {'uris': track_uris}
    if position is not None:
        payload['position'] = position
    return (
        'POST', '/users/{}/playlists/{}/tracks'.format(user_id, playlist_id), {}, payload
    )


def user_playlist_tracks_remove_all_occurences(user_id, playlist_id, track_uris, snapshot_id=None):
    payload = {'tracks': [{'uri': uri} for uri in track_uris]}
    if snapshot_id:
        payload['snapshot_id'] = snapshot_id
    return (
        'DELETE', '/users/{}/playlists/{}/tracks'.format(user_id, playlist_id), {}, payload
    )


def user_playlist_tracks_remove_specific_occurences(user_id, playlist_id, tracks, snapshot_id=None):
    """
    tracks: list of {'uri': 'something', positions: [0,4,6]} objects
    """
    payload = {'tracks': tracks}
    if snapshot_id:
        payload['snapshot_id'] = snapshot_id
    return (
        'DELETE', '/users/{}/playlists/{}/tracks'.format(user_id, playlist_id), {}, payload
    )


def me_player_devices():
    return 'GET', '/me/player/devices'

def search(q, type, limit=50, offset=0, market=None):
    return 'GET', '/search', dict(q=q, type=type, limit=limit, offset=offset, market=market)


def me_player_currently_playing(market=None):
    return 'GET', '/me/player/currently-playing', {'market': market}


def me_player_play(device_id=None, context_uri=None, uris=None, offset=None):
    return (
        'PUT', '/me/player/play', {'device_id': device_id},
        {'context_uri': context_uri, 'uris': uris, 'offset': offset}
    )


def me_player_pause(device_id=None):
    return 'PUT', '/me/player/pause', {'device_id': device_id}


def me_player_next(device_id=None):
    return 'POST', '/me/player/next', {'device_id': device_id}


def me_player_previous(device_id=None):
    return 'POST', '/me/player/previous', {'device_id': device_id}


def me_player_volume(volume_percent, device_id=None):
    return 'PUT', '/me/player/volume', {
        'volume_percent': volume_percent, 'device_id': device_id
    }



@_deco
def _clear_none_params(function, *args, **kwargs):
    """
    Decorator to clear any None value query and payload params from
    endpoint function results.
    """
    result = function(*args, **kwargs)
    if 'params' in result:
        result['params'] = {k: v for k,
                            v in result['params'].items() if v is not None}
    if 'payload' in result:
        result['payload'] = {k: v for k,
                             v in result['payload'].items() if v is not None}
    return result


@_deco
def _tuple_to_dict(function, *args, **kwargs):
    rtuple = function(*args, **kwargs)
    result = {}
    keys = ('method', 'url', 'params', 'payload')
    for i, value in enumerate(rtuple):
        result[keys[i]] = value
    return result


# Apply _clear_none_params decorator to all endpoint functions in this module
_current_module = _sys.modules[__name__]


def _is_resource(obj):
    return (
        _inspect.isfunction(obj)
        and obj.__module__ == __name__
        and not obj.__name__.startswith('_')
    )


_endpoints = {}

for name, function in _inspect.getmembers(_current_module, _is_resource):
    function = _clear_none_params(_tuple_to_dict(function))
    _endpoints[name] = function
    setattr(_current_module, name, function)

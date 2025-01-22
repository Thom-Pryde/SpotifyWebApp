import datetime
import requests
from flask import Blueprint, Response, redirect, session
from spotify_app.auth import API_BASE_URL

playlist_blueprint = Blueprint('playlist', __name__)










# Playlist Route (Fetches the user's playlists)
@playlist_blueprint.route('/playlist')
def get_playlist():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    # Request to get the user's playlists from Spotify
    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)

    playlist_data = response.json()

    playlist_links = [
        f"<a href='/playlist/{item['id']}/tracks'>{item['name']}</a>"
        for item in playlist_data['items']
    ]
    formatted_links = "<br>".join(playlist_links)

    html_content = f"""
    <html>
        <head><title>User Playlists</title></head>
        <body>
            <h1>Your Playlists</h1>
            {formatted_links}
        </body>
    </html>
    """
    return Response(html_content, content_type='text/html; charset=utf-8')

# Playlist Tracks Route (Fetches tracks for a specific playlist)
@playlist_blueprint.route('/playlist/<playlist_id>/tracks')
def get_playlist_tracks(playlist_id):
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    # Request to get the playlist's tracks
    response = requests.get(f"{API_BASE_URL}playlists/{playlist_id}/tracks", headers=headers)
    playlist_tracks = response.json()

    track_list = [
        f"{track['track']['name']} by {', '.join([artist['name'] for artist in track['track']['artists']])}"
        for track in playlist_tracks['items']
    ]
    
    html_content = f"""
    <html>
        <head><title>Tracks in Playlist</title></head>
        <body>
            <h1>Tracks in Playlist</h1>
            <ul>
                {"".join([f"<li>{track}</li>" for track in track_list])}
            </ul>
        </body>
    </html>
    """
    return Response(html_content, content_type='text/html; charset=utf-8')

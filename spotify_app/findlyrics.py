import datetime
import requests
from flask import Blueprint, jsonify, request, Response, redirect, session, render_template
import urllib.parse
from spotify_app.auth import API_BASE_URL,GENIUS_CLIENT_ACCESS_TOKEN,GENIUS_CLIENT_ID
import lyricsgenius as lg
import logging

findlyrics_blueprint = Blueprint('findlyrics', __name__)


#Genius_Client_Access_Token
#Genius_Client_ID
@findlyrics_blueprint.route('/findlyrics')
def findlyrics():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    return render_template('findlyrics.html')


@findlyrics_blueprint.route('/findlyrics_api')
def findlyrics_api():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL + 'me/player/currently-playing', headers=headers,)
    if response.status_code == 200:
        data = response.json()
        track_name = data['item']['name']
        #print("Track Name:",track_name)
        artist_name = data['item']['artists'][0]['name']
    else:
        logging.error("Failed to fetch currently playing track from Spotify.")
        return jsonify({'error': 'Could not fetch currently playing track.'}), 500
        #print("Artist Name:",artist_name)
   
    # genius= lg.Genius(GENIUS_CLIENT_ACCESS_TOKEN)
    #proxy = {"http": "http://103.25.155.233:83","https": "https://103.25.155.233:83"}
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    genius = lg.Genius(GENIUS_CLIENT_ACCESS_TOKEN,user_agent)
    
    try:
        song = genius.search_song(title=track_name, artist=artist_name)
        if song and song.lyrics:
            lyrics = song.lyrics
            return jsonify({'track_name':track_name,'artist_name': artist_name, 'lyrics': lyrics})
        else:
            logging.warning(f"No lyrics found for: {track_name} by {artist_name}")
            return jsonify({'track_name': track_name, 'artist_name': artist_name, 'lyrics': 'No lyrics available.'})
    except Exception as e:
        logging.error(f"Error while searching for lyrics: {e}")
        return jsonify({'error': 'An error occurred while fetching lyrics.'}), 500








# @findlyrics_blueprint.route('/test_genius_api')
# def test_genius_api():
#     try:
#         headers = {'Authorization': f"Bearer {GENIUS_CLIENT_ACCESS_TOKEN}"}
#         response = requests.get(
#             "https://api.genius.com/search",
#             headers=headers,
#             params={"q": "Hello Adele"}
#         )
#         response.raise_for_status()
#         return jsonify(response.json())
#     except requests.exceptions.HTTPError as e:
#         return jsonify({'error': f"HTTPError: {str(e)}"}), 500
#     except Exception as e:
#         return jsonify({'error': f"Unexpected error: {str(e)}"}), 500
import datetime
import requests
from flask import Blueprint, jsonify, request, Response, redirect, session, render_template
import urllib.parse
from auth import API_BASE_URL,GENIUS_CLIENT_ACCESS_TOKEN,GENIUS_CLIENT_ID
import lyricsgenius as lg

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
        #print("Artist Name:",artist_name)

    genius= lg.Genius(GENIUS_CLIENT_ACCESS_TOKEN)
    song = genius.search_song(title=track_name, artist=artist_name)
    lyrics  = song.lyrics
    return jsonify({'track_name':track_name,'artist_name': artist_name, 'lyrics': lyrics})



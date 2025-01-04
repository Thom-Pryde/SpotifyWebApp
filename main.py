import datetime
import requests
from flask import Flask, redirect, request, session, jsonify, Response
import urllib.parse 
import re
import emoji
import json
app = Flask(__name__)
app.secret_key ='sdfsdf7039809uf093fus'

CLIENT_ID = '4fcdf09bcb424abba5cd5e16d77c2c24'
CLIENT_SECRET = '4498f7349b5045c6a8e3b77025703e6c'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize' # url to get token from spotify, refresh token, api base url too
TOKEN_URL = 'https://accounts.spotify.com/api/token' #Where we resfresh the token
API_BASE_URL = 'https://api.spotify.com/v1/'




@app.route('/')
def index():
    return "welcome to spotify app by thombo <a href='/login'>Login with spotify</a>" #redirect to login page

#need to make a login end point where ill be reduirecting them to spotifys login page 
#declare persmission scope from spotify
#so need to redirect or make a request to spotify api saying we want the user to loginb and say what permissions theyll give us

@app.route('/login')
def login():
    #scope = 'user-read-private user-read-email playlist-read-private playlist-read-collaborative' #og
    #scope = 'playlist-read-private playlist-read-collaborative user-read-private user-library-read'
    scope = 'playlist-read-private playlist-read-collaborative user-read-private user-library-read user-top-read user-read-playback-state user-read-recently-played'


    #spotify make us pass paramters when calling request
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True 
        #when they come back to page, as acccess token, they dont need to login again. good for testing take out later
    }

    #instead of using a get req they just redirect to their url as thats whats on documentation
    auth_url = f'{AUTH_URL}?{urllib.parse.urlencode(params)}'
    return redirect(auth_url)


#all this is to make a req to spotifys auth url, parse params including scope () to get private stuff, then redirect to spotifys login page

#call back endpoint, this is the cal that spotify wil come back to once they login. if success theyll give us a code to give us access. or they give us error..

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    #no errrors: successfull login
    #if successful theryll give back a code paramater, we need to use send this code to spotifys token url to get access token
    if 'code' in request.args:
        req_body = {
            'code' : request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
            #we have the req body ready, time to send to spotify.
        response = requests.post(TOKEN_URL, data=req_body)
        #reponse from spotify, theyll give token ino as json object
        token_info = response.json()
        print(token_info)  # Add this to inspect the token_info


        session['access_token'] = token_info['access_token'] #access token
        session['refresh_token'] = token_info['refresh_token'] #refresh token
        session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']  #timestamp when token expires
        #cuurent time, turn into time stamp, number seconds + 36000. time stamp when token expires


        return redirect('/homepage') #redirect to playlist page
        #end point to retreive users playlist

@app.route('/homepage')
def homepage():

    html_content = """
    <html>
    <body>
        <h1>Welcome to the Spotify App</h1>


        <p>Click the button below to view your playlists:</p>
        <form action="/playlist" method="get">
            <button type="submit">View Playlists</button>
        </form>
        <p>Click the button below to view your top songs:</p>
        <form action="/topsongs" method="get">
            <button type="submit">View Top Songs</button>
        </form>
    </body>
    </html>
    """
    return Response(html_content, content_type='text/html; charset=utf-8')


@app.route('/topsongs')
def get_topsongs():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:  # expired
        return redirect('/refresh_token')

    html_content = """
    <html>
        <head>
            <title>User Top Songs</title>
            <script>
                function fetchTopSongs(time_range) {
                    fetch('/topsongs_api?time_range=' + time_range)
                        .then(response => response.json())
                        .then(data => {
                            // Display the song names and artists in a simple list
                            //console.log('Test');
                            let songList = data.items.map((item,index) => index + 1 + ' '+ item.name + ' by ' + item.artists.map(artist => artist.name).join(', ')).join('<br>');
                            document.getElementById('top-songs').innerHTML = songList || 'No songs found.';
                        })
                        .catch(error => {
                            console.error('Error fetching top songs:', error);
                            document.getElementById('top-songs').innerHTML = 'Error loading songs.';
                        });
                }

            </script>
        </head>
        <body>
            <button onclick="fetchTopSongs('short_term')">~Last 4 Weeks</button>
            <button onclick="fetchTopSongs('medium_term')">~Last 6 Months</button>
            <button onclick="fetchTopSongs('long_term')">~Last Year</button>
            <h1>Your Top Songs</h1>
            <div id="top-songs"></div>
        </body>
    </html>
    """
    return Response(html_content, content_type='text/html; charset=utf-8')



@app.route('/topsongs_api')
def get_topsongs_api():

    if 'access_token' not in session:
        return redirect('/login')
     
    if datetime.datetime.now().timestamp() > session['expires_at']: #expired in past
        return redirect('/refresh_token')
    headers = {
        'Authorization': f"Bearer {session['access_token']}" #access token in auth header
    }

    time_range = request.args.get('time_range')
    print('Time Range:', time_range)
    limit = 20
    params = {
        'time_range': time_range,
        'limit': limit
    }

    response = requests.get(API_BASE_URL + 'me/top/tracks', headers=headers,params=params)  
    print('API Response Status Code:', response.status_code)
    #print('API Response Body:', response.text)

    if response.status_code == 200:
         data = response.json()


         for item in data.get('items', []):
            #print(item['name'])
            for key, value in item.items():
                print(key, value)

         return jsonify(data)  # Return JSON data with the correct response format
    
    else:
        return jsonify({"error": "Failed to fetch top songs", "status_code": response.status_code}), response.status_code



















@app.route('/playlist')
def get_playlist():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']: #expired in past
        return redirect('/refresh_token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}" #access token in auth header
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers) #store the result of makign the req to end point
    #print(f"Playlist request status code: {response.status_code}")
    #print(f"Response content: {response.text}")

    playlist_data = response.json()
    #playlist_names = [item['name'] for item in playlist_data['items']]
    playlist_links = [
        f"<a href='/playlist/{item['id']}/tracks'>{item['name']}</a>"  # Playlist name links to the tracks route
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

    #return Response(formatted_links, content_type='text/plain; charset=utf-8')
   # return Response(
      #  json.dumps(playlist_names, ensure_ascii=False),
       # content_type='application/json; charset=utf-8'
    #)   

    #return jsonify(playlist_names)

@app.route('/playlist/<playlist_id>/tracks')
def get_playlist_tracks(playlist_id):
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']: #expired in past
        return redirect('/refresh_token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}" #access token in auth header
    }
    response = requests.get(f"{API_BASE_URL}playlists/{playlist_id}/tracks", headers=headers)
    
    tracks_data = response.json()
    #print(f"Response content: {response.text}")

    # track_ids = []
    # for item in tracks_data.get('items', []):
    #     track = item.get('track') #get track dict
    #     if track and 'id' in track:  
    #         track_ids.append(track['id'])

    # for id in track_ids:
    #     # response = requests.get(f"{API_BASE_URL}tracks/{id}", headers=headers)
    #     # track_info_all = response.json()
    #     # print(f"Track data: {track_info_all}")
    #     response = requests.get(f"{API_BASE_URL}audio-features/{id}", headers=headers)

    
        # if response.status_code == 200:
        #     track_analysis = response.json()
        #     #print(track_analysis.get('track', {}).get ('key'))
        #     print(f"Track ID: {id}, Key: {track_analysis.get('key')}")
        # #print(f"Track data: {track_analysis}")
        # else:
        #     print(f"Failed to fetch track analysis for track ID {id}: {response.status_code}")
        # if response.status_code == 200:
        #     analysis_data = response.json()
        #     track_data = analysis_data.get('track', {})
        #     key = track_data.get('key', -1)
        #     key_confidence = track_data.get('key_confidence', 0)
        #     print(f"Key: {key} (Confidence: {key_confidence})")
        # else:
        #     print(f"Failed to fetch data: {response.status_code} - {response.reason}")



    track_list = [
        f"{item['track']['name']} by {', '.join(artist['name'] for artist in item['track']['artists'])}"
        for item in tracks_data.get('items', [])
    ]
    #print(track_list)

    #spotify reponse is in the form items : track{ name, artists{ name} } ect or track{"artists":  {"name": "Artist A"}, {"name": "Artist B"}  so need loop
    
    formatted_tracks = "<br>".join(track_list)

    html_content = f"""
    <html>
        <head><title>Playlist Tracks</title></head>
        <body>
            <h1>Tracks in Playlist</h1>
            {formatted_tracks if formatted_tracks else '<p> playlist is empty :( .</p>'}
        </body>
    </html>
    """

    return Response(html_content, content_type='text/html; charset=utf-8')    



#token refresh endpoint
@app.route('/refresh_token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    #is in session, but has access token expired?
    if datetime.datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',  
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json() #contains new access token and expires in 

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.datetime.now().timestamp() + new_token_info['expires_in'] #new expirey time

        return redirect('/playlist')
    




if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True) #run the app, host
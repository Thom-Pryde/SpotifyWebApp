import datetime
import requests
from flask import Blueprint, jsonify, request, Response, redirect, session
from auth import CLIENT_ID, API_BASE_URL

topsongs_blueprint = Blueprint('topsongs', __name__)

# Top Songs Route (Renders the HTML and provides buttons for time ranges)
@topsongs_blueprint.route('/topsongs')
def get_topsongs():
    if 'access_token' not in session:
        return redirect('/login')

    # Check if the token has expired and refresh if necessary
    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')

    html_content = """
    <html>
        <head>
            <title>User Top Songs</title>
            <script>
                // JavaScript function to fetch top songs for the selected time range
                function fetchTopSongs(time_range) {
                    fetch('/topsongs_api?time_range=' + time_range)
                        .then(response => response.json())
                        .then(data => {
                            let songList = data.items.map((item,index) => index + 1 + ' ' + item.name + ' by ' + item.artists.map(artist => artist.name).join(', ')).join('<br>');
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

# Top Songs API Route (Fetches user's top tracks from Spotify's API)
@topsongs_blueprint.route('/topsongs_api')
def get_topsongs_api():
    if 'access_token' not in session:
        return redirect('/login')

    # Check if the token has expired and refresh if necessary
    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    time_range = request.args.get('time_range')
    limit = 1
    params = {
        'time_range': time_range,
        'limit': limit
    }

    # Request to fetch the top tracks
    response = requests.get(API_BASE_URL + 'me/top/tracks', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
       
            



        # for track_url in data['items']:
        #     track_url = track_url['external_urls']['spotify']
        #     print(track_url)


        print("Top response keys:", data.keys())
        print()
        for item in data['items']:
            print(f"Item keys:")
            for key in item.keys():
                print(key)
            print()
            


        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch top songs", "status_code": response.status_code}), response.status_code

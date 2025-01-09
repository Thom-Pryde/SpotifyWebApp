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
                // JavaScript function to fetch top songs for the selected time range they choose from da button
                function fetchTopSongs(time_range) {
                    fetch('/topsongs_api?time_range=' + time_range)
                        .then(response => response.json())
                        .then(data => {
                            let songList = data.items.map((item,index) => { //not a singl expression and now a body block so need {} and return
                                let albumpic = item.album.images[2].url;
                                let albumdate = item.album.release_date;
                                let duration_ms = item.duration_ms/1000 + " seconds";
                                let popularity = item.popularity + "%"; 

                                return `<div>
                                    <img src = "${albumpic}" alt = "">
                                    ${index + 1}. ${item.name} by ${item.artists.map(artist => artist.name).join(', ')}
                                    ${albumdate} 
                                    ${duration_ms}
                                    ${popularity}
                                    <a href= "${item.external_urls.spotify}" target = "_blank">Listen on Spotify</a>


                                </div>
                                `;

                            }).join('<br>'); // Join the array of songs with a line gapp

                            
                            document.getElementById('top-songs').innerHTML = songList || 'No songs found.';
                        })//then data close
                        
                        .catch(error => {
                            console.error('Error fetching top songs:', error);
                            document.getElementById('top-songs').innerHTML = 'Error loading songs.';
                        });
                }//fetchTopSongs close
            </script>
        </head>
        <body>
            <div class="top-container">
                <h1 class = "title"> Your Top Songs</h1>
                <div class="top-buttons">
                    <button onclick="fetchTopSongs('short_term')">~Last 4 Weeks</button>
                    <button onclick="fetchTopSongs('medium_term')">~Last 6 Months</button>
                    <button onclick="fetchTopSongs('long_term')">~Last Year</button>
                </div>
            </div>
            <div id="top-songs"></div>
        </body>
    </html>
    """
    return Response(html_content, content_type='text/html; charset=utf-8')



@topsongs_blueprint.route('/song_details_api')
def get_song_details_api():

    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    ids = request.args.get('ids')
    if not ids:
        return jsonify({"error": "No IDs provided"}), 400


    params = {
        'ids': ids
    }
    print("Requested Song IDs: ", ids)
    response = requests.get(API_BASE_URL + 'tracks', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch da song deets", "status_code": response.status_code}), response.status_code














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
    limit = 8
    params = {
        'time_range': time_range,
        'limit': limit
    }

    # Request to fetch the top tracks
    response = requests.get(API_BASE_URL + 'me/top/tracks', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
       
        for item in data['items']:
            print(f"external url: {item['external_urls']}")



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

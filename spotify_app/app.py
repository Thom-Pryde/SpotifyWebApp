from flask import Flask, redirect, Response, url_for, session, render_template
from spotify_app.auth import auth_blueprint
from spotify_app.topsongs import topsongs_blueprint
from spotify_app.playlist import playlist_blueprint
from spotify_app.artistsearch import artistsearch_blueprint
from spotify_app.findlyrics import findlyrics_blueprint
import datetime
import requests
import os
from spotify_app.auth import CLIENT_ID, API_BASE_URL
import logging
# from dotenv import load_dotenv
if os.getenv('FLASK_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from the .env file
app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Register blueprints for modular routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(topsongs_blueprint)
app.register_blueprint(playlist_blueprint)
app.register_blueprint(artistsearch_blueprint)
app.register_blueprint(findlyrics_blueprint)

logging.basicConfig(
    level=logging.INFO,  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Print logs to console
    ]
)



def get_userdata():
    # print(session['access_token'])
    if 'access_token' not in session:
        logging.error('no acess token in session')
        return None, None, None, None, None
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL + 'me', headers=headers)
    #logging.info(f"Spotify API Status: {response.status_code}, Response: {response.text}")

    if response.status_code == 401:
        logging.error('Acess token expired or just invalid')
        return None, None, None, None
    try:
        user_data = response.json()
        country = user_data['country']
        link = user_data['external_urls']['spotify']
        name = user_data['display_name']
        followers = user_data['followers']['total']
        profilepic = user_data['images'][0]['url'] if user_data['images'] else None
        return ( country,link, name, followers, profilepic)
    except Exception as e:
        logging.error(f"Error parsing user data: {e}")
        return None, None, None, None, None


    #recently played grab:)


def get_recently_played():
    if 'access_token' not in session:
        logging.error('no acess token in session')
        return None
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    limit = 5
    params = {
        'limit': limit
    }
    recently_played_response = requests.get(API_BASE_URL + 'me/player/recently-played',headers=headers, params=params)

    if recently_played_response.status_code == 401:
        logging.error('Access token expired or invalid when calling /me/player/recently-played')
        return None
    if recently_played_response.status_code != 200:
        logging.error(f"Error {recently_played_response.status_code} retrieving recently played tracks")
        return None  
    
    try:
        recently_played_data = recently_played_response.json()
    except Exception as e:
        logging.error(f"Error parsing recently played data: {e}")
        return None
        

    items = recently_played_data.get('items', [])
    parsed_items = []
    for item in items:
        track = item["track"]  
        played_at = format_timestamp(item["played_at"])

        track_name = track["name"]     
        artists = track["artists"]           
        album = track["album"]        
        artist_names = ", ".join(artist["name"] for artist in artists)
        album_images = album["images"]       
        album_image = album_images[1]["url"] if album_images else None

        parsed_items.append({
            'played_at': played_at,
            'track_name': track_name,
            'artist_names': artist_names,
            'album_image': album_image,
        })
        
    return parsed_items


def format_timestamp(iso_timestamp):
    date_part, time_part = iso_timestamp.split("T")
    time_part = time_part.split(".")[0] 
    formatted_time = datetime.datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
    hour_24 = formatted_time.strftime("%H:%M") 
    am_pm = "AM" if formatted_time.hour < 12 else "PM"
    return f"{formatted_time.strftime('%b %dth, at')} {hour_24} {am_pm}" 
 #jan 29 2025 08:58 PM





@app.route('/')
def index():
    # print("Inside index route")
    # Check if the user is logged in (i.e., if 'access_token' is in the session)
    # logged_in = 'access_token' in session
    

    # if logged_in:
    #     if 'expires_at' in session and datetime.datetime.now().timestamp() > session['expires_at']:
    #         # token has expired-- refresh it
    #         return redirect('/refresh_token')
    #     country, link, name, followers, profilepic = get_userdata()

    # else:
    #     country = None
    #     link = None
    #     name = None
    #     followers = None
    #     profilepic = None
    logged_in = 'access_token' in session
    tracks = None
    if logged_in:
        if 'expires_at' in session and datetime.datetime.now().timestamp() > session['expires_at']:
            logging.info("Access token expired. Redirecting to refresh.")
            return redirect('/refresh_token')
        country, link, name, followers, profilepic = get_userdata()
        tracks = get_recently_played()


        if not all([country, link, name, followers, profilepic]):
            logging.error("Failed to fetch user data. Clearing session and showing homepage.")
            session.clear()
            logged_in = False #Mark them as logged out
    else:
        #User is not logged in
        country, link, name, followers, profilepic = None, None, None, None, None

    return render_template('homepage.html', logged_in = logged_in, country = country, link = link, name = name, followers = followers, profilepic = profilepic, tracks=tracks)


if __name__ == "__main__":
    # print("Flask app is starting")
    # app.run(debug=True)
     app.run()










    # html_content = f"""
    # <html>
    # <head>
    #     <title>Wrapify Home</title>
    #         <link rel="stylesheet" type="text/css" href="{ url_for('static', filename='css/stylesHP.css') }">
    #         <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap" rel="stylesheet">
    # </head>

    # <body class="homepagebody">
    #     <nav class="navbar">
    #         <div class="logo-container">
    #                 <h1 class="logo">Wrapify</h1>
    #             </div>
    #         <ul> 
    #             <li>
    #                 <a href="{ '/topsongs' if logged_in else '#'}" 
    #                 class="{'nav-link disabled' if not logged_in else 'nav-link'}">Top Songs</a>
    #             </li>
    #             <li>
    #                 <a href="{ '/playlist' if logged_in else '#'}" 
    #                 class="{'nav-link disabled' if not logged_in else 'nav-link'}">Playlists</a>
    #             </li>
    #             <li>
    #                 <a href="/login" class="get_started {'hidden' if logged_in else ''}">Get Started</a>
    #             </li>
    #         </ul>
    #     </nav>

    #     <main> 
    #         <div class="main_overall_page">
    #             <p> </p>
    #         </div>
    #     </main>
    # </body>
    # </html>
    # """
    
    # return html_content
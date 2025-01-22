from flask import Flask, redirect, Response, url_for, session, render_template
from auth import auth_blueprint
from topsongs import topsongs_blueprint
from playlist import playlist_blueprint
from artistsearch import artistsearch_blueprint
from findlyrics import findlyrics_blueprint
import datetime
import requests
import os
from auth import CLIENT_ID, API_BASE_URL
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Register blueprints for modular routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(topsongs_blueprint)
app.register_blueprint(playlist_blueprint)
app.register_blueprint(artistsearch_blueprint)
app.register_blueprint(findlyrics_blueprint)




def get_userdata():
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL + 'me', headers=headers)
    user_data = response.json()
    country = user_data['country']
    link = user_data['external_urls']['spotify']
    name = user_data['display_name']
    followers = user_data['followers']['total']
    profilepic = user_data['images'][0]['url']
    

    return ( country,link, name, followers, profilepic)





@app.route('/')
def index():
    # print("Inside index route")
    # Check if the user is logged in (i.e., if 'access_token' is in the session)
    logged_in = 'access_token' in session


    if logged_in:
        if 'expires_at' in session and datetime.datetime.now().timestamp() > session['expires_at']:
            # token has expired-- refresh it
            return redirect('/refresh_token')
        country, link, name, followers, profilepic = get_userdata()

    else:
        country = None
        link = None
        name = None
        followers = None
        profilepic = None
    return render_template('homepage.html', logged_in = logged_in, country = country, link = link, name = name, followers = followers, profilepic = profilepic)


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
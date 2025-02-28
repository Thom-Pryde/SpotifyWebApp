import datetime
import requests
from flask import Blueprint, redirect, request, session, jsonify
import urllib.parse
# from dotenv import load_dotenv
import os
import logging

if os.getenv('FLASK_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from the .env file
# load_dotenv()  # Load the environment variables from the .env file
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

GENIUS_CLIENT_ACCESS_TOKEN = os.getenv('GENIUS_CLIENT_ACCESS_TOKEN')
GENIUS_CLIENT_ID = os.getenv('GENIUS_CLIENT_ID')

auth_blueprint = Blueprint('auth', __name__)

#REDIRECT_URI = 'http://localhost:5000/callback'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
AUTH_URL = 'https://accounts.spotify.com/authorize'
API_BASE_URL = 'https://api.spotify.com/v1/'  # Spotify API base URL

# Login Route (Step 1: User Login)
@auth_blueprint.route('/login')
def login():
    # print(f"REDIRECT_URI: {REDIRECT_URI}")
    # Define the scope of permissions requested from Spotify
    #scope = 'playlist-read-private playlist-read-collaborative user-read-private user-library-read user-top-read user-read-playback-state user-read-recently-played user-read-currently-playing'
    scope = 'user-read-private user-read-email user-read-currently-playing user-top-read user-read-recently-played'







#playlist-read-private: Access to private playlists.

#playlist-read-collaborative: Access to collaborative playlists.

#user-library-read: Access to the user's saved tracks and albums.

#user-read-playback-state: Access to the user's current playback state.

#user-read-recently-played: Access to the user's recently played tracks.






    # Build the authorization URL with the necessary parameters
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True  # Forces the user to log in each time
    }
    
    # Redirect the user to Spotify's authorization page
    auth_url = f'{AUTH_URL}?{urllib.parse.urlencode(params)}'
    return redirect(auth_url)

# Callback Route (Step 2: Receive the code and exchange it for an access token)
@auth_blueprint.route('/callback')
def callback():
    # Handle potential errors during the callback
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    # If we receive the authorization code, exchange it for an access token
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        
        # Request the access token from Spotify's API
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        
        # Save the token details in the session
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']

        return redirect('/')
        #return redirect('/homepage')

#Refresh Token Route (Handles token expiration and refresh)
@auth_blueprint.route('/refresh_token')
def refresh_token():
    # # If the refresh token is not in the session, redirect to login
    # if 'refresh_token' not in session:
    #     logging.error("No refresh token found in session. Redirecting to login.")
    #     return redirect('/login')

    # # Request to refresh the access token using the stored refresh token
    # req_body = {
    #     'grant_type': 'refresh_token',
    #     'refresh_token': session['refresh_token'],
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET
    # }

    # response = requests.post(TOKEN_URL, data=req_body)
    # token_info = response.json()

    # # Update the session with the new access token
    # session['access_token'] = token_info['access_token']
    # session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']
    
    # return redirect('/')
    # #return redirect('/homepage')
        # If the refresh token is not in the session, redirect to login
    if 'refresh_token' not in session:
        logging.error("No refresh token found in session. Redirecting to login.")
        return redirect('/login')

    logging.info("Attempting to refresh access token...")

    # Request to refresh the access token using the stored refresh token
    req_body = {
        'grant_type': 'refresh_token',
        'refresh_token': session['refresh_token'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    try:
        response = requests.post(TOKEN_URL, data=req_body)
        response.raise_for_status()  # Raise an exception for HTTP errors

        token_info = response.json()

        # Debugging: Log the full response
        logging.info(f"Token refresh response: {token_info}")

        # Ensure the response contains the new access token
        if 'access_token' in token_info:
            session['access_token'] = token_info['access_token']
            session['expires_at'] = datetime.datetime.now().timestamp() + token_info.get('expires_in', 3600)
            logging.info("Access token refreshed successfully.")
        else:
            logging.error("Access token not found in response. Redirecting to login.")
            return redirect('/login')

    except requests.exceptions.RequestException as e:
        logging.error(f"Error refreshing token: {e}")
        return redirect('/login')

    return redirect('/')

@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect('/')   

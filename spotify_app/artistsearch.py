import datetime
import requests
from flask import Blueprint, jsonify, request, Response, redirect, session, render_template
import urllib.parse
from spotify_app.auth import CLIENT_ID, API_BASE_URL

artistsearch_blueprint = Blueprint('artistsearch', __name__)

@artistsearch_blueprint.route('/artistsearch')
def artistsearch():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    return render_template('artistsearch.html')


@artistsearch_blueprint.route('/artistsearch_api')
def get_artistsearch_api():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    search_query = request.args.get('search_query')
    if not search_query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    limit = 10
    params = {
        "q": search_query,   
        'limit': limit,
        "type": "track", 
    }

    response = requests.get(API_BASE_URL + 'search', headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
       
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch top songs", "status_code": response.status_code}), response.status_code




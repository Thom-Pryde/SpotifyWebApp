import datetime
import requests
from flask import Blueprint, jsonify, request, Response, redirect, session, render_template
from auth import CLIENT_ID, API_BASE_URL

topsongs_blueprint = Blueprint('topsongs', __name__)


@topsongs_blueprint.route('/topsongs')
def get_topsongs():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    return render_template('topsongs.html')



#api call for top songs 
@topsongs_blueprint.route('/topsongs_api')
def get_topsongs_api():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    time_range = request.args.get('time_range')
    limit = 7
    params = {
        'time_range': time_range,
        'limit': limit
    }

    # Request to fetch the top tracks
    response = requests.get(API_BASE_URL + 'me/top/tracks', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
       
        # for item in data['items']:
        #     print(f"external url: {item['external_urls']}")



        # for track_url in data['items']:
        #     track_url = track_url['external_urls']['spotify']
        #     print(track_url)


        # print("Top response keys:", data.keys())
        # print()
        # for item in data['items']:
        #     print(f"Item keys:")
        #     for key in item.keys():
        #         print(key)
        #     print()
            


        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch top songs", "status_code": response.status_code}), response.status_code






# #not used anymore
# @topsongs_blueprint.route('/song_details_api')
# def get_song_details_api():

#     if 'access_token' not in session:
#         return redirect('/login')

#     if datetime.datetime.now().timestamp() > session['expires_at']:
#         return redirect('/refresh_token')

#     headers = {
#         'Authorization': f"Bearer {session['access_token']}"
#     }

#     ids = request.args.get('ids')
#     if not ids:
#         return jsonify({"error": "No IDs provided"}), 400


#     params = {
#         'ids': ids
#     }
#     print("Requested Song IDs: ", ids)
#     response = requests.get(API_BASE_URL + 'tracks', headers=headers, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         return jsonify(data)
#     else:
#         return jsonify({"error": "Failed to fetch da song deets", "status_code": response.status_code}), response.status_code


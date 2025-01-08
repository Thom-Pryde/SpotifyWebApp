from flask import Flask, redirect, Response, url_for, session
from auth import auth_blueprint
from homepage import homepage_blueprint
from topsongs import topsongs_blueprint
from playlist import playlist_blueprint
import datetime

app = Flask(__name__)
app.secret_key = 'sdfsdf7039809uf093fus'

# Register blueprints for modular routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(homepage_blueprint)
app.register_blueprint(topsongs_blueprint)
app.register_blueprint(playlist_blueprint)

@app.route('/')
def index():
    # Check if the user is logged in (i.e., if 'access_token' is in the session)
    logged_in = 'access_token' in session
    if logged_in and 'expires_at' in session:
        if datetime.datetime.now().timestamp() > session['expires_at']:
            # token has expired-- refresh it
            return redirect('/refresh_token')
    html_content = f"""
    <html>
    <head>
        <title>Wrapify Home</title>
        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='styles.css')}">
        <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap" rel="stylesheet">
    </head>

    <body>
        <nav class="navbar">
            <h1 class="logo">Wrapify</h1>
            <div class="navcontainer">
                <ul> 
                    <li>
                        <a href="{ '/topsongs' if logged_in else '#'}" 
                        class="{'nav-link disabled' if not logged_in else 'nav-link'}">Top Songs</a>
                    </li>

                    <li>
                        <a href="{ '/playlist' if logged_in else '#'}" 
                        class="{'nav-link disabled' if not logged_in else 'nav-link'}">Playlists</a>
                    </li>

                    <li>
                        <a href="/login" class="get_started {'hidden' if logged_in else ''}">Get Started</a>
                    </li>


                </ul>
            </div>
        </nav>

        <main> 
            <div class="main_overall_page">
                <p> Driven by a love for music, this website expands on the information Spotify doesn't show, using their APIs to provide deeper insights 
                into artists, albums, and tracks. It's designed to give you more details and help you explore music in a whole new way.</p>
            </div>
        </main>
    </body>
    </html>
    """
    
    return html_content

























#before new idea
# @app.route('/')
# def index():
#     html_content = f"""
#     <html>
#     <head>
#         <title>Wrapify Home</title>
#         <link rel="stylesheet" type="text/css" href="{url_for('static', filename='styles.css')}">
#     </head>


#     <body class = "main_overall_page">

#         <div class = "main_header_div">
#             <h1 class = "logo"> Wrapify </h1>
#             <a class = "link" href='/login'>Login with Spotify here</a>  
#         </div>

#     </body>


#     </html>
#     """
#     return html_content























#<h1 class= "bottom_header">bomba </h1>






# @app.route('/')
# def index():
#     #return "welcome to spotify app by thombo <a href='/login'>Login with spotify</a>" #redirect to login page

#     html_content = """
#     <html>
#     <head>
#         <link rel="stylesheet" type="text/css" href="{url_for('static', filename='styles.css')}">
#     </head>
#     <body>
#         <h1>Thombo's Spotify</h1>
#         <a href='/login'>Login with spotify here</a>
#     </body>
#     </html>
#     """
#     return Response(html_content, content_type='text/html; charset=utf-8')










if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, redirect, Response, url_for, session, render_template
from auth import auth_blueprint
from topsongs import topsongs_blueprint
from playlist import playlist_blueprint
import datetime

app = Flask(__name__)
app.secret_key = 'sdfsdf7039809uf093fus'

# Register blueprints for modular routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(topsongs_blueprint)
app.register_blueprint(playlist_blueprint)

@app.route('/')
def index():
    print("Inside index route")
    # Check if the user is logged in (i.e., if 'access_token' is in the session)
    logged_in = 'access_token' in session
    if logged_in and 'expires_at' in session:
        if datetime.datetime.now().timestamp() > session['expires_at']:
            # token has expired-- refresh it
            return redirect('/refresh_token')

    return render_template('homepage.html', logged_in=logged_in)

if __name__ == "__main__":
    print("Flaskkkkkkkkkkk app is starting")
    app.run(debug=True)










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
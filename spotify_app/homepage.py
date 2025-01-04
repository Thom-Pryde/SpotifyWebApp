from flask import Blueprint, Response, url_for

homepage_blueprint = Blueprint('homepage', __name__)

# Homepage Route
@homepage_blueprint.route('/homepage')
def homepage():
    # HTML content for the homepage
    html_content = f"""
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='styles.css')}">
    </head>
    <body>
    
        <h1 >Welcome to the Wrapify</h1>

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

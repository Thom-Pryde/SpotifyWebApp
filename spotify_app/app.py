from flask import Flask, redirect, Response, url_for
from auth import auth_blueprint
from homepage import homepage_blueprint
from topsongs import topsongs_blueprint
from playlist import playlist_blueprint

app = Flask(__name__)
app.secret_key = 'sdfsdf7039809uf093fus'

# Register blueprints for modular routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(homepage_blueprint)
app.register_blueprint(topsongs_blueprint)
app.register_blueprint(playlist_blueprint)


@app.route('/')
def index():
    html_content = f"""
    <html>
    <head>
        <title>Wrapify Home</title>
        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='styles.css')}">
    </head>


    <body class = "main_overall_page">

        <div class = "main_header_div">
            <h1 class = "logo"> Wrapify </h1>
            <a class = "link" href='/login'>Login with Spotify here</a>  
        </div>

    </body>


    </html>
    """
    return html_content



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

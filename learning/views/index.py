"""
Learning app index (main) view.

URLs include:
/
/login
/login/callback
/logout
"""
import flask
import learning
import json
import os
import requests

from learning.views.matches import matches
from learning.views.form import form
from learning.db import get_conn

from oauthlib.oauth2 import WebApplicationClient
from flask_login import (
        current_user,
        login_required,
        login_user,
        logout_user,
)
from learning.user import User

conn = get_conn()

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

#Table Creation
# cursor=conn.cursor()
# create_table="""
# create table Matches (name varchar(200),email varchar(200),comment varchar(200) )

# """
# cursor.execute(create_table)

# def send_to_matches():
#     cur = conn.cursor()
#     cur.execute("SELECT *  FROM Details")
#     details = cur.fetchall()

@learning.app.route('/')
def show_index():
    """Display / route."""
    if current_user.is_authenticated:
        context = {"name": current_user.name}
    else:
        context = {}
    return flask.render_template("index.html", **context)

@learning.app.route("/login")
def login():
    # Get redirect
    redirect = flask.request.args.get('next')
    flask.session['redirect'] = redirect

    # Find out what URL to hit for Google login
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=flask.request.base_url + "/callback",
        scope=["openid", "email", "profile"],
        prompt="login",
    )
    return flask.redirect(request_uri)

@learning.app.route("/login/callback")
def callback():
    # Get redirect
    redirect = flask.session['redirect']


    # Get authorization code Google sent back to you
    code = flask.request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=flask.request.url,
        redirect_url=flask.request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Limit access to umich students
    if users_email.split('@')[1] != "umich.edu":
        flask.flash("Please use your umich email.")
        return flask.redirect(flask.url_for("show_index"))

    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database. (Register user)
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user to form/matches
    return flask.redirect(redirect)


@learning.app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for("show_index"))

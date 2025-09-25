import os
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request, render_template_string
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from Strava_Get_Activity_IDs import get_activity_ids
from Strava_Get_LatLng import get_latlng
from Stations_Visited_pd import stations_visited
from Stations_Visited_by_Activity import stations_visited_per_activity

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET KEY", "dev_secret")

login_manager = LoginManager()
login_manager.init_app(app)

users = {}


class User(UserMixin):
    def __init__(self, strava_id, token):
        self.id = strava_id
        self.token = token

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template_string("""
                    <h1>Welcome!</h1>
                    <p>You are logged in as Strava athlete {{ user.id }}</p>
                    <a href="{{ url_for('profile') }}">View Strava profile</a><br>
                    <a href="{{ url_for('logout') }}">Logout</a>
                """, user=current_user)
    return '<a href="/login">Login with Strava</a>'

@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    auth_url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&scope=read,activity:read"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Missing code from Strava!", 400

    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    r = requests.post(token_url, data=payload)
    data = r.json()

    strava_id = str(data["athlete"]["id"])
    token = data["access_token"]
    user = User(strava_id, token)
    users[strava_id] = user
    login_user(user)

    return redirect(url_for("home"))

@app.route("/profile")
@login_required
def profile():
    headers = {"Authorization": f"Bearer {current_user.token}"}
    r = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)
    profile_data = r.json()
    return render_template_string("""
            <h1>Your Strava Profile</h1>
            <p>Name: {{ p.firstname }} {{ p.lastname }}</p>
            <p>City: {{ p.city }}</p>
            <p>Country: {{ p.country }}</p>
            <a href="{{ url_for('home') }}">Back</a>
        """, p=profile_data)

# @app.route("/sync")
# @login_required
# def sync():
#     get_activity_ids()
#     get_latlng()
#     stations_visited()
#     stations_visited_per_activity()

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import random

app = Flask(__name__)
app.secret_key = 'supersecret123'
authifyID = random.randint(1000000,9999999)

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id="652923225802-u1cr7qet7i6ckjrsjfv509fbbq7hi4fj.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
    api_base_url='https://openidconnect.googleapis.com/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo'

)


@app.route("/")
def home():
    user = session.get("user")
    return render_template("homepage.html", user = user, authifyID = authifyID)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/google")
def login_google():
    redirect_uri = url_for('callback', _external=True)
    print("Redirect URI:", redirect_uri)
    return google.authorize_redirect(redirect_uri)

@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['user'] = user_info

    return redirect("verification")

@app.route("/verification")
def verification():
    user = session.get("user")
    return render_template("verification.html", user = user)

@app.route("/verifyafriend")
def verifyafriend():
    user = session.get("user")
    return render_template("verifyfriend.html",user = user)


@app.route("/logout")
def logout():
    session.pop("user", None) 
    return redirect("/")        


if __name__ == "__main__":
    app.run(debug=True)

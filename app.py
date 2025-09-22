from flask import Flask, render_template, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'supersecret123'

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='652923225802-u1cr7qet7i6ckjrsjfv509fbbq7hi4fj.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo',  # Get user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route("/")
def home():
    return render_template("homepage.html")

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
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

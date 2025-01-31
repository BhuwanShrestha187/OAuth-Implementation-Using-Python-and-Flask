import os
from flask import Flask, redirect, url_for, session, render_template, request, flash
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import pyodbc

app = Flask(__name__)
app.secret_key = "your_secret_key"

# OAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='GOOGLE_CLIENT_ID',
    client_secret='GOOGLE_CLIENT_SECRET',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',  # Add this line
    client_kwargs={'scope': 'openid email profile'},
)

# SQL Server Connection
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=BhuwanPC;" 
    "DATABASE=FlaskAuthDB;"
    "Trusted_Connection=yes;"  # Enables Windows Authentication
)


# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    @staticmethod
    def get_by_email(email):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = ?", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return User(id=user_data[0], name=user_data[1], email=user_data[2])
        return None


users = {}

@login_manager.user_loader
def load_user(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE Id = ?", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        return User(id=user_data[0], name=user_data[1], email=user_data[2])
    return None


@app.route('/')
def home():
    return render_template("login.html")  # Render the improved UI


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = ?", (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            if user_data[3] == password:  # Using plain text comparison for now
                user = User(id=user_data[0], name=user_data[1], email=user_data[2])
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid password! Please try again.", "danger")  # Inform user in UI
        else:
            flash("No account found with that email!", "danger")

    return render_template("login.html")






@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    user = User(id=user_info['id'], name=user_info['name'], email=user_info['email'])
    users[user.id] = user
    login_user(user)
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    return f"<h1>Welcome {current_user.name}</h1> <a href='/logout'>Logout</a>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

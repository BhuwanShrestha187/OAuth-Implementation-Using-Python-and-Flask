import os
import random
from flask import Flask, redirect, url_for, session, render_template, request, flash
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import pyodbc
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

app = Flask(__name__)
app.secret_key = "your_secret_key"

#Necessary Steps added for the Forgot Password Functionality: 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ayanshrestha187@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'szrx ltkh ksgx ynri'  # Replace with an app password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)


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
        password = request.form['password']  # User-entered password

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = ?", (email,))
        user_data = cursor.fetchone()

        if user_data:
            stored_hashed_password = user_data[3]  # Get hashed password (Check your column order)
            
            # Check if the entered password matches the hashed password
            if check_password_hash(stored_hashed_password, password):
                session['user_id'] = user_data[0]  # Store user ID in session
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))  # Redirect to dashboard
            else:
                flash("Incorrect password. Please try again.", "danger")
        else:
            flash("Email not found. Please register.", "danger")

    return render_template("login.html")







@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    user = User(id=user_info['id'], name=user_info['name'], email=user_info['email'])
    users[user.id] = user
    login_user(user)
    return redirect(url_for('dashboard'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = ?", (email,))
        user_data = cursor.fetchone()

        if user_data:
            reset_code = str(random.randint(100000, 999999))  # Generate 6-digit code

            # Store reset code in the database
            cursor.execute("UPDATE Users SET ResetCode = ? WHERE Email = ?", (reset_code, email))
            conn.commit()

            # Send email to user
            msg = Message("Password Reset Code", recipients=[email])
            msg.body = f"Your password reset code is: {reset_code}"
            mail.send(msg)

            flash("A reset code has been sent to your email.", "success")
            return redirect(url_for("verify_code", email=email))
        else:
            flash("No account found with this email!", "danger")

    return render_template("forgot_password.html")


@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    email = request.args.get('email')

    if request.method == 'POST':
        entered_code = request.form['code']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email = ? AND ResetCode = ?", (email, entered_code))
        user_data = cursor.fetchone()

        if user_data:
            session['reset_email'] = email  # Store email in session
            return redirect(url_for("reset_password"))
        else:
            flash("Invalid verification code!", "danger")

    return render_template("verify_code.html", email=email)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        return redirect(url_for("forgot_password"))

    if request.method == 'POST':
        new_password = request.form['password']
        email = session['reset_email']

        hashed_password = generate_password_hash(new_password)  # Secure password hashing

        cursor = conn.cursor()
        cursor.execute("UPDATE Users SET PasswordHash = ?, ResetCode = NULL WHERE Email = ?", (hashed_password, email))
        conn.commit()

        flash("Your password has been updated! You can now log in.", "success")
        session.pop('reset_email', None)
        return redirect(url_for("login"))

    return render_template("reset_password.html")




@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "danger")
        return redirect(url_for("login"))
    
    return render_template("dashboard.html")


@app.route('/logout')
def logout():
    session.clear()  # ✅ Clears all session data
    flash("You have been logged out.", "info")  # ✅ Optional message
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)

# 🔐 Flask Authentication System with Google OAuth

## 📌 Overview
This is a **Flask-based authentication system** that allows users to:
- Register and log in using **email and password**
- Log in using **Google OAuth**
- Reset their password if forgotten
- Access a secure **dashboard** after authentication
- Logout securely

This project follows **best security practices** including password hashing and session management.

## 🚀 Features
✅ **User Authentication:** Sign Up, Login, Logout  
✅ **Password Reset:** Forgot Password, Email Verification, Reset Password  
✅ **Google OAuth Login**  
✅ **Dashboard (Protected Page)**  
✅ **Session Management & Security**  
✅ **Bootstrap-based Responsive UI**  
✅ **Flask-Mail for sending verification emails**  
✅ **Flask-Login for secure authentication handling**  

---

## 🏗️ Tech Stack
**Backend:** Flask, Flask-Login, Flask-Mail, Authlib, PyODBC  
**Frontend:** HTML, CSS (Bootstrap), JavaScript  
**Database:** SQL Server (or SQLite/MySQL/PostgreSQL)  

---

## 📂 Project Structure
```
FlaskAuthApp/
│── templates/
│   ├── login.html
│   ├── register.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── verify_code.html
│   ├── dashboard.html
│── static/
│   ├── styles.css  # Additional CSS
│── app.py  # Main application logic
│── requirements.txt  # Required dependencies
│── README.md  # Project documentation
```

---

## 🛠️ Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/FlaskAuthApp.git
cd FlaskAuthApp
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Database (SQL Server)
Ensure SQL Server is installed and running. Modify **app.py** with your database credentials:
```python
conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=YourServerName;DATABASE=FlaskAuthDB;Trusted_Connection=yes;"
)
```
Create the `Users` table:
```sql
CREATE TABLE Users (
    Id INT PRIMARY KEY IDENTITY,
    Username VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PasswordHash VARCHAR(255),
    ResetCode VARCHAR(6) NULL
);
```

### 5️⃣ Configure Email Service (Flask-Mail)
Edit **app.py** with your email credentials (use environment variables for security):
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

### 6️⃣ Set Up Google OAuth (Optional)
1. Go to [Google Developer Console](https://console.cloud.google.com/)
2. Create a new project → Enable OAuth 2.0
3. Get **Client ID** and **Client Secret**
4. Add them to **app.py**:
```python
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://oauth2.googleapis.com/token',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)
```

### 7️⃣ Run the Application
```bash
python app.py
```
The app will be available at: **http://127.0.0.1:5000/**

---

## 🧪 Testing the Application
✅ **Register a New User**  
✅ **Login with Email and Password**  
✅ **Login with Google OAuth**  
✅ **Try Password Reset & Email Verification**  
✅ **Check if session management works properly**  

---

## 🔒 Security Measures Implemented
🔹 **Password Hashing** (Using `werkzeug.security`)  
🔹 **Session Management** (Flask-Login)  
🔹 **CSRF Protection** (Flask-WTF if added later)  
🔹 **OAuth 2.0 Implementation**  
🔹 **Environment Variables for Sensitive Data**  

---

## 🛠️ Future Improvements
- ✅ Add JWT-based authentication for API support
- ✅ Implement Two-Factor Authentication (2FA)
- ✅ Add email confirmation upon signup

---

## 👨‍💻 Contributors
📌 **Bhuwan Shrestha** – Developer

Feel free to contribute by opening **issues** or **pull requests**!

---

## ⭐ Support & Feedback
If you found this project helpful, **star** 🌟 this repo and share your feedback!

Happy Coding! 🚀


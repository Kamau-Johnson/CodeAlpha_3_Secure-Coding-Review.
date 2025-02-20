from flask import Flask, request, render_template, redirect, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from  import Limiter
from import get_remote_address

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")


limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

def get_db_connection():
    conn = sqlite3.connect("database.db")
    return conn

@app.route("/")
def home():
    return "Welcome to the secure app!"

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")  
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,)) 
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):  
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  

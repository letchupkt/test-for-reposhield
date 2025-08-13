from flask import Flask, request, render_template
import sqlite3
import os
import utils

app = Flask(__name__)

# 🚨 Vulnerable: Hardcoded secret key
app.secret_key = "supersecretkey123"

# 🚨 Insecure: Database in same folder
DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    # 🚨 SQL Injection vulnerability
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username LIKE '%{query}%'")
    results = c.fetchall()
    conn.close()
    return {"results": results}

@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_password = utils.weak_hash(password)  # 🚨 Weak hash
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    return {"status": "User added"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)

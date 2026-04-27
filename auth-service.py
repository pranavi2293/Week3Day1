import sqlite3
from flask import Flask, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        
        user = cursor.execute(query).fetchone()
    except Exception as e:
        return f"Database Error: {str(e)}", 500

    if user:
        
        return {
            "message": "Login successful",
            "username": user[0],
            "password": user[1],
            "ssn": user[2]  # <--- CRITICAL PRIVACY LEAK
        }, 200
    
    return "Access Denied", 401

if __name__ == '__main__':
    # We keep the 0.0.0.0 so the test can actually reach the "Bad" code
    app.run(host='0.0.0.0', port=5000)
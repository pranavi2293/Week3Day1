import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db_connection()
    
    query = "SELECT username FROM users WHERE username = ? AND password = ?"
    user = conn.execute(query, (username, password)).fetchone()
    conn.close()

    if user:
        
        return jsonify({"message": "Login successful", "user": user['username']}), 200
    
    return "Access Denied", 401

if __name__ == '__main__':
   
    app.run(host='0.0.0.0', port=5000)
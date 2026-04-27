from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

# Home page (basic UI)
@app.route('/')
def home():
    return render_template("week3.html")

# GET all users
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    data = [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
    return jsonify(data)

# POST create user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                 (data['name'], data['email']))
    conn.commit()
    conn.close()
    return {"message": "User added"}

# DELETE user
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"message": "User deleted"}

if __name__ == "__main__":
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.close()
    app.run(debug=True)
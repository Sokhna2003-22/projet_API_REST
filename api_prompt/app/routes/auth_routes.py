from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import psycopg2
from config import DATABASE

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT id, role FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()

    if user:
        access_token = create_access_token(identity={"id": user[0], "role": user[1]})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Identifiants incorrects"}), 401

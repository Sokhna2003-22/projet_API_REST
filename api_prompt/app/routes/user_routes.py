
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
from config import DATABASE

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({'msg': 'Accès interdit'}), 403
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users")
    users = cur.fetchall()
    return jsonify(users)

@user_routes.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({'msg': 'Accès interdit'}), 403
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    return jsonify({'msg': 'Utilisateur supprimé'})
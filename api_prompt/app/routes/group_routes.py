from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
from config import DATABASE

group_routes = Blueprint('group_routes', __name__)

@group_routes.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM groups")
    groups = cur.fetchall()
    return jsonify(groups)

@group_routes.route('/groups/<int:id>/add_user/<int:user_id>', methods=['POST'])
@jwt_required()
def add_user_to_group(id, user_id):
    user = get_jwt_identity()
    if user['role'] != 'admin':
        return jsonify({'msg': 'Accès interdit'}), 403
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("UPDATE users SET group_id = %s WHERE id = %s", (id, user_id))
    conn.commit()
    return jsonify({'msg': 'Utilisateur ajouté au groupe'})
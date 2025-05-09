from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
from config import DATABASE

vote_routes = Blueprint('vote_routes', __name__)

@vote_routes.route('/prompts/<int:prompt_id>/vote', methods=['POST'])
@jwt_required()
def vote(prompt_id):
    user = get_jwt_identity()
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    # Vérifie si l'utilisateur a déjà voté
    cur.execute("SELECT * FROM votes WHERE user_id = %s AND prompt_id = %s", (user['id'], prompt_id))
    if cur.fetchone():
        return jsonify({'msg': 'Déjà voté'}), 400
    # Calcul des points en fonction du groupe
    cur.execute("SELECT group_id FROM users WHERE id = (SELECT user_id FROM prompts WHERE id = %s)", (prompt_id,))
    prompt_group_id = cur.fetchone()[0]
    cur.execute("SELECT group_id FROM users WHERE id = %s", (user['id'],))
    user_group_id = cur.fetchone()[0]
    point = 2 if prompt_group_id == user_group_id else 1
    cur.execute("INSERT INTO votes (user_id, prompt_id, value) VALUES (%s, %s, %s)", (user['id'], prompt_id, point))
    conn.commit()
    return jsonify({'msg': 'Vote enregistré', 'points': point})
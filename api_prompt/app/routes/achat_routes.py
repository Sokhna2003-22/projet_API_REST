from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request_optional
import psycopg2
from config import DATABASE

achat_routes = Blueprint('achat_routes', __name__)

@achat_routes.route('/prompts/<int:prompt_id>/buy', methods=['POST'])
def acheter(prompt_id):
    user_id = None
    try:
        verify_jwt_in_request_optional()
        user = get_jwt_identity()
        if user:
            user_id = user['id']
    except:
        pass
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO achats (user_id, prompt_id) VALUES (%s, %s)", (user_id, prompt_id))
    conn.commit()
    return jsonify({'msg': 'Achat enregistré'})
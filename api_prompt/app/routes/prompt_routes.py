
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
from config import DATABASE

prompt_routes = Blueprint('prompt_routes', __name__)

@prompt_routes.route('/prompts', methods=['POST'])
@jwt_required()
def create_prompt():
    user = get_jwt_identity()
    data = request.get_json()
    content = data.get("content")

    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO prompts (content, user_id, state) VALUES (%s, %s, %s)", (content, user['id'], 'en_attente'))
    conn.commit()
    return jsonify({'msg': 'Prompt ajouté avec succès'})

@prompt_routes.route('/prompts', methods=['GET'])
def list_prompts():
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM prompts")
    prompts = cur.fetchall()
    return jsonify(prompts)

@prompt_routes.route('/prompts/search', methods=['GET'])
def search_prompts():
    q = request.args.get('q', '')
    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM prompts WHERE content ILIKE %s", ('%' + q + '%',))
    results = cur.fetchall()
    return jsonify(results)
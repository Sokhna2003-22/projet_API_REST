
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
from config import DATABASE

note_routes = Blueprint('note_routes', __name__)

@note_routes.route('/prompts/<int:prompt_id>/note', methods=['POST'])
@jwt_required()
def noter(prompt_id):
    user = get_jwt_identity()
    data = request.get_json()
    score = data.get("score")

    conn = psycopg2.connect(**DATABASE)
    cur = conn.cursor()

    # Vérifie si l'utilisateur a déjà noté ce prompt
    cur.execute("SELECT * FROM notes WHERE user_id = %s AND prompt_id = %s", (user['id'], prompt_id))
    if cur.fetchone():
        return jsonify({"msg": "Vous avez déjà noté ce prompt"}), 400

    # Enregistrer la note
    cur.execute("INSERT INTO notes (user_id, prompt_id, score) VALUES (%s, %s, %s)", (user['id'], prompt_id, score))
    conn.commit()

    # Recalculer la note moyenne et mettre à jour le prix
    cur.execute("""
        SELECT n.score, u.group_id FROM notes n
        JOIN users u ON u.id = n.user_id
        WHERE prompt_id = %s
    """, (prompt_id,))
    notes = cur.fetchall()

    cur.execute("SELECT group_id FROM users WHERE id = (SELECT user_id FROM prompts WHERE id = %s)", (prompt_id,))
    auteur_group = cur.fetchone()[0]

    total = 0
    for n, gid in notes:
        total += n * (0.6 if gid == auteur_group else 0.4)
    moyenne = total / len(notes)
    nouveau_prix = 1000 * (1 + moyenne)

    cur.execute("UPDATE prompts SET prix = %s WHERE id = %s", (nouveau_prix, prompt_id))
    conn.commit()

    return jsonify({'msg': 'Note enregistrée', 'moyenne': moyenne, 'prix': nouveau_prix})
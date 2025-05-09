import psycopg2
from flask import Flask
from config import DATABASE

def create_app():
    app = Flask(__name__)
    
    app.config['JWT_SECRET_KEY'] = 'sokhna99'

    try:
        conn = psycopg2.connect(**DATABASE)
        print("Connexion à la BDD réussie !")
    except Exception as e:
        print("Erreur de connexion à la BDD :", e)

    return app

from flask_jwt_extended import JWTManager

jwt = JWTManager()
jwt.init_app(app)

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.routes.auth_routes import auth
from app.routes.user_routes import user_routes
from app.routes.group_routes import group_routes
from app.routes.prompt_routes import prompt_routes
from app.routes.vote_routes import vote_routes
from app.routes.note_routes import note_routes
from app.routes.achat_routes import achat_routes
import psycopg2
from config import DATABASE

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'sokhna99'

    jwt = JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(user_routes)
    app.register_blueprint(group_routes)
    app.register_blueprint(prompt_routes)
    app.register_blueprint(vote_routes)
    app.register_blueprint(note_routes)
    app.register_blueprint(achat_routes)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'msg': 'Route non trouvée'}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'msg': 'Erreur interne du serveur'}), 500

    return app

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.database import db
from src.schemas import ma
from src.resources.blacklist_check_resource import BlacklistResource
from src.resources.blacklist_resource import BlacklistCheckResource
import os


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuración de base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///local.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "secret123")

    # Inicialización
    db.init_app(app)
    ma.init_app(app)
    JWTManager(app)

    api = Api(app)

    # Recursos RESTful (OOP)
    api.add_resource(BlacklistResource, "/blacklists")
    api.add_resource(BlacklistCheckResource, "/blacklists/<string:email>")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

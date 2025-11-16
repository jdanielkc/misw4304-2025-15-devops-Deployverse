from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from .database import db
from .schemas import ma
from .resources.blacklist_check_resource import BlacklistResource
from .resources.blacklist_resource import BlacklistCheckResource


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    # Configuración por defecto - PostgreSQL RDS
    db_uri = (
        "postgresql://postgres:uniandes-db-pssw@"
        "blacklistdb.c1i64e8wqk6h.us-east-1.rds.amazonaws.com:5432/"
        "blacklistdb"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "secret123"

    # Aplicar configuración personalizada si se proporciona (para tests)
    if config:
        app.config.update(config)

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


if __name__ == "__main__":
    # Create and run the app only when executed as a script. This avoids
    # starting the development server during imports (e.g. pytest).
    _app = create_app()
    _app.run(host="0.0.0.0", port=5000, debug=True)

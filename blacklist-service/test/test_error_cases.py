import json
from src.app import create_app
from src.database import db
from src.models import BlacklistEntry

def test_add_blacklist_entry_unauthorized():
    """Test POST sin autorización"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        client = app.test_client()

        res = client.post(
            "/blacklists",
            json={
                "email": "test@example.com",
                "app_uuid": "1234-uuid",
                "blocked_reason": "testing"
            },
            headers={"Authorization": "Bearer WrongToken"}
        )
        assert res.status_code == 401
        data = res.get_json()
        assert data["error"] == "Unauthorized"

def test_add_blacklist_entry_missing_fields():
    """Test POST con campos faltantes"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        client = app.test_client()

        res = client.post(
            "/blacklists",
            json={
                "email": "test@example.com"
                # Falta app_uuid
            },
            headers={"Authorization": "Bearer BearerToken123"}
        )
        assert res.status_code == 400
        data = res.get_json()
        assert data["error"] == "Missing required fields"

def test_add_blacklist_entry_duplicate_email():
    """Test POST con email duplicado"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        
        # Agregar entrada inicial
        entry = BlacklistEntry(
            email="duplicate@example.com",
            app_uuid="uuid-1",
            blocked_reason="first entry",
            ip_address="127.0.0.1"
        )
        db.session.add(entry)
        db.session.commit()
        
        client = app.test_client()

        # Intentar agregar el mismo email
        res = client.post(
            "/blacklists",
            json={
                "email": "duplicate@example.com",
                "app_uuid": "uuid-2",
                "blocked_reason": "duplicate"
            },
            headers={"Authorization": "Bearer BearerToken123"}
        )
        assert res.status_code == 400
        data = res.get_json()
        assert data["error"] == "Email already exists or database error"
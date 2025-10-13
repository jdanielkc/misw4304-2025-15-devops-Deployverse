from src.app import create_app
from src.database import db
from src.models import BlacklistEntry

def test_get_blacklist_entry():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        # Limpiar cualquier dato existente
        db.session.query(BlacklistEntry).delete()
        db.session.commit()
        
        db.session.add(BlacklistEntry(
            email="john@example.com",
            app_uuid="uuid-1",
            blocked_reason="spam",
            ip_address="127.0.0.1"
        ))
        db.session.commit()

        client = app.test_client()
        res = client.get(
            "/blacklists/john@example.com",
            headers={"Authorization": "Bearer BearerToken123"}
        )

        assert res.status_code == 200
        data = res.get_json()
        assert data["blacklisted"] is True
        assert data["entry"]["email"] == "john@example.com"

def test_get_blacklist_entry_unauthorized():
    """Test GET sin autorización"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        client = app.test_client()
        
        res = client.get(
            "/blacklists/test@example.com",
            headers={"Authorization": "Bearer WrongToken"}
        )
        
        assert res.status_code == 401
        data = res.get_json()
        assert data["error"] == "Unauthorized"

def test_get_blacklist_entry_not_found():
    """Test GET para email no en blacklist"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        client = app.test_client()
        
        res = client.get(
            "/blacklists/notfound@example.com",
            headers={"Authorization": "Bearer BearerToken123"}
        )
        
        assert res.status_code == 200
        data = res.get_json()
        assert data["blacklisted"] is False

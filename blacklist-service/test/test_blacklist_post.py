import json
from src.app import create_app
from src.database import db

def test_add_blacklist_entry():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    }
    app = create_app(config=test_config)

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
            headers={"Authorization": "Bearer BearerToken123"}
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["email"] == "test@example.com"

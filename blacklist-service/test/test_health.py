from src.app import create_app
from src.database import db

def test_health_endpoint():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    }
    app = create_app(config=test_config)

    with app.app_context():
        db.create_all()
        client = app.test_client()

        res = client.get("/health")
        assert res.status_code == 200
        data = res.get_json()
        assert data["status"] == "ok"
from flask import request
from flask_restful import Resource
from src.models import BlacklistEntry
from src.schemas import BlacklistSchema
from src.database import db
import os

STATIC_TOKEN = os.getenv("STATIC_TOKEN", "BearerToken123")
blacklist_schema = BlacklistSchema()

class BlacklistResource(Resource):
    def post(self):
        auth = request.headers.get("Authorization")
        if auth != f"Bearer {STATIC_TOKEN}":
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        if not data or "email" not in data or "app_uuid" not in data:
            return {"error": "Missing required fields"}, 400

        entry = BlacklistEntry(
            email=data["email"],
            app_uuid=data["app_uuid"],
            blocked_reason=data.get("blocked_reason"),
            ip_address=request.remote_addr
        )

        db.session.add(entry)
        try:
            db.session.commit()
            return blacklist_schema.dump(entry), 201
        except Exception as e:
            db.session.rollback()
            return {"error": "Email already exists or database error"}, 400

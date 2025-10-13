from flask_restful import Resource
from flask import request
from src.models import BlacklistEntry
from src.schemas import BlacklistSchema
import os

STATIC_TOKEN = os.getenv("STATIC_TOKEN", "BearerToken123")
blacklist_schema = BlacklistSchema()

class BlacklistCheckResource(Resource):
    def get(self, email):
        auth = request.headers.get("Authorization")
        if auth != f"Bearer {STATIC_TOKEN}":
            return {"error": "Unauthorized"}, 401

        entry = BlacklistEntry.query.filter_by(email=email).first()
        if not entry:
            return {"blacklisted": False}, 200

        return {
            "blacklisted": True,
            "entry": blacklist_schema.dump(entry)
        }, 200

from flask_marshmallow import Marshmallow
from .models import BlacklistEntry

ma = Marshmallow()


class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlacklistEntry
        load_instance = True

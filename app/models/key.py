from app.Blueprints import db

class Key(db.Model):
    __tablename__ = "api_key"
    id = db.Column('id', db.Integer, primary_key = True)
    key = db.Column('unique_key', db.Unicode)
    fr = db.Column('for', db.Unicode)